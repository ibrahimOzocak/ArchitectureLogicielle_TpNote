<template>
  <div>
    <h1>MES Quizz</h1>
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
import { ref } from 'vue'
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
      fetch('http://127.0.0.1:5000/questionnaires', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData)
      })
      .then(response => {
          if (response.ok) {
              console.log('Questionnaire créé avec succès !');
              // Mettre à jour l'interface utilisateur
              this.fetchQuestionnaires();
          } else {
              // Gérer les erreurs de création du questionnaire
              console.error('Erreur lors de la création du questionnaire :', response.status);
          }
      })
      .catch(error => {
          console.error('Erreur lors de la création du questionnaire :', error);
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
          console.log('Nom du questionnaire modifié avec succès !');
          // Mettre à jour l'interface utilisateur
          this.fetchQuestionnaires();
        } else {
          // Gérer les erreurs de modification du nom du questionnaire
          console.error('Erreur lors de la modification du nom du questionnaire :', response.status);
        }
      })
      .catch(error => {
        console.error('Erreur lors de la modification du nom du questionnaire :', error);
      });
    },

    deleteQuestionnaire(questionnaireId) {
    // Récupérer les questions associées au questionnaire
      fetch(`http://127.0.0.1:5000/questionnaires/${questionnaireId}/questions`)
          .then(response => response.json())
          .then(data => {
              // Supprimer chaque question associée au questionnaire
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

              // Une fois que toutes les questions sont supprimées, supprimer le questionnaire lui-même
              Promise.all(deletePromises)
                  .then(() => {
                      fetch(`http://127.0.0.1:5000/questionnaires/${questionnaireId}`, {
                          method: 'DELETE',
                          headers: {
                              'Content-Type': 'application/json'
                          }
                      })
                      .then(response => {
                          if (response.ok) {
                              console.log('Questionnaire supprimé avec succès !');
                              // Mettre à jour l'interface utilisateur
                              this.fetchQuestionnaires();
                          } else {
                              // Gérer les erreurs de suppression du questionnaire
                              console.error('Erreur lors de la suppression du questionnaire :', response.status);
                          }
                      })
                      .catch(error => {
                          console.error('Erreur lors de la suppression du questionnaire :', error);
                      });
                  });
          })
          .catch(error => {
              console.error('Erreur lors de la récupération des questions associées au questionnaire :', error);
          });
    },
    
    ajouterQuestions(questionnaireId) {
      const title = prompt("Entrez le titre de la question :");
      const formData = {
        title: title,
        questionnaire_id: questionnaireId
      };
      fetch(`http://127.0.0.1:5000/questionnaires/${questionnaireId}/questions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      })
      .then(response => {
        if (response.ok) {
          console.log('Question ajoutée avec succès !');
          // Si la question a été ajoutée avec succès, mettre à jour l'interface utilisateur
          this.fetchQuestionnaires();
        } else {
          // Gérer les erreurs d'ajout de question
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
          console.error('Erreur lors de la récupération des questionnaires :', error);
        });
    }
  },
  components: {
    Questionnaire
  }
}
</script>



