<template>
  <div>
    <h1>Mes Quizz</h1>
    <input type="button" value="Ajouter un questionnaire" @click="creerQuestionnaire">
    <ul>
      <Questionnaire v-for="questionnaire in questionnaires"
                     :key="questionnaire.id"
                     :questionnaire="questionnaire"
                     @ajouterQuestion="ajouterQuestions"
                     @modifierNomQuestionnaire="modifierNomQuestionnaire"
                     @deleteQuestionnaire="deleteQuestionnaire" />
    </ul>
  </div>
</template>

<script>
import Questionnaire from './components/Questionnaire.vue';

export default {
  data() {
    return {
      questionnaires: []
    }
  },
  mounted() {
    this.fetchQuestionnaires();
  },
  methods: {
    creerQuestionnaire() {
      const newQuestionnaire = prompt("Entrez le nom du nouveau questionnaire :");
      const formData = {
          name: newQuestionnaire
      };
      if (newQuestionnaire == null || newQuestionnaire == ""){return;}
      fetch('http://127.0.0.1:5000/questionnaires', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData)
      })
      .then(response => {
          if (response.ok) {
              console.log('Questionnaire crÃ©Ã© avec succÃ¨s !');
              // Mettre Ã  jour l'interface utilisateur
              this.fetchQuestionnaires();
          } else {
              console.error('Erreur lors de la crÃ©ation du questionnaire :', response.status);
          }
      })
      .catch(error => {
          console.error('Erreur lors de la crÃ©ation du questionnaire :', error);
      });
    },
    modifierNomQuestionnaire(questionnaireId) {
      const nouveauNom = prompt("Entrez le nouveau nom du questionnaire :", this.questionnaires.name);
      const formData = {
        name: nouveauNom
      };
      fetch(`http://127.0.0.1:5000/questionnaires/${questionnaireId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      })
      .then(response => {
        if (response.ok) {
          console.log('Nom du questionnaire modifiÃ© avec succÃ¨s !');
          this.fetchQuestionnaires();
        } else {
          console.error('Erreur lors de la modification du nom du questionnaire :', response.status);
        }
      })
      .catch(error => {
        console.error('Erreur lors de la modification du nom du questionnaire :', error);
      });
    },

    deleteQuestionnaire(questionnaireId) {
    // RÃ©cupere les questions du questionnaire
      fetch(`http://127.0.0.1:5000/questionnaires/${questionnaireId}/questions`)
          .then(response => response.json())
          .then(data => {
              // Supprime les questions du questionnaire
              const deletePromises = data.questions.map(question => {
                  return fetch(`http://127.0.0.1:5000/questionnaires/${questionnaireId}/questions/${question.id}`, {
                      method: 'DELETE'
                  })
                  .then(response => {
                      if (!response.ok) {
                          console.error(`Erreur lors de la suppression de la question ${question.id} :`, response.status);
                      }
                  })
                  .catch(error => {
                      console.error(`Erreur lors de la suppression de la question ${question.id} :`, error);
                  });
              });

              // suprimme le questionnaire
              Promise.all(deletePromises)
              // promise.all sert a verifier si toutes les questions sont supprimÃ©es
                  .then(() => {
                      fetch(`http://127.0.0.1:5000/questionnaires/${questionnaireId}`, {
                          method: 'DELETE',
                          headers: {
                              'Content-Type': 'application/json'
                          }
                      })
                      .then(response => {
                          if (response.ok) {
                              console.log('Questionnaire supprimÃ© avec succÃ¨s !');
                              this.fetchQuestionnaires();
                          } else {
                              console.error('Erreur lors de la suppression du questionnaire :', response.status);
                          }
                      })
                      .catch(error => {
                          console.error('Erreur lors de la suppression du questionnaire :', error);
                      });
                  });
          })
          .catch(error => {
              console.error('Erreur lors de la rÃ©cupÃ©ration des questions associÃ©es au questionnaire :', error);
          });
    },
    
    ajouterQuestions(questionnaireId) {
      const title = prompt("Entrez le titre de la question :");
      const formData = {
        title: title,
        questionnaire_id: questionnaireId
      };
      if (title == null || title == ""){return;}
        fetch(`http://127.0.0.1:5000/questionnaires/${questionnaireId}/questions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      })
      .then(response => {
        if (response.ok) {
          console.log('Question ajoutÃ©e avec succÃ¨s !');
          this.fetchQuestionnaires();
        } else {
          console.error('Erreur lors de l\'ajout de la question :', response.status);
        }
      })
      .catch(error => {
        console.error('Erreur lors de l\'ajout de la question :', error);
      });
    },
    fetchQuestionnaires() {
      fetch('http://127.0.0.1:5000/questionnaires')
        .then(response => response.json())
        .then(data => {
          this.questionnaires = data.questionnaires;
        })
        .catch(error => {
          console.error('Erreur lors de la rÃ©cupÃ©ration des questionnaires :', error);
        });
    }
  },
  components: {
    Questionnaire
  }
}
</script>



