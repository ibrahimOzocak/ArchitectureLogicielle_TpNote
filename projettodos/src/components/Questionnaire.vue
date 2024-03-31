<template>
    <div>
      <div v-if="questionnaire">
        <p><strong>Nom :</strong> {{ questionnaire.name }}</p>
        <input type="button"
        class="btn btn-danger"
        value="MODIFIER" @click="modifierNomQuestionnaire">
        <input type="button"
        class="btn btn-danger"
        value="SUPPRIMER" @click="deleteQuestionnaire">
        <input type="button"
        class="btn btn-danger"
        value="AJOUTER QUESTION" @click="ajouterQuestion">
        <div>
          <ul>
            <Question v-for="question in questions"
            :key="question.id"
            :question="question"
            @editQuestion="editQuestion"
            @deleteQuestion="deleteQuestion">
                {{ question.title }}
            </Question>
          </ul>
        </div>
      </div>
      <div v-else>
        <p>Aucun questionnaire sélectionné.</p>
      </div>
    </div>
  </template>
  
  
  <script>
  import Question from './Question.vue';

  export default {
    data() {
      return {
        questions: []
      };
    },
    props: {
      questionnaire: Object
    },
    mounted() {
      this.fetchQuestionnaires()
    },
    methods: {
        deleteQuestion(questionId) {
            fetch(`http://127.0.0.1:5000/questionnaires/${this.questionnaire.id}/questions/${questionId}`, {
                method: 'DELETE'
            })
            .then(response => {
                if (response.ok) {
                // Suppression réussie, mettre à jour l'interface utilisateur
                this.questions = this.questions.filter(question => question.id !== questionId);
                } else {
                // Gérer les erreurs de suppression
                console.error('Erreur lors de la suppression de la question :', response.status);
                }
            })
            .catch(error => {
                console.error('Erreur lors de la suppression de la question :', error);
            });
        },
        editQuestion(questionId) {
            const questionToUpdate = this.questions.find(question => question.id === questionId);
            const newTitle = prompt('Entrez le nouveau titre de la question :', questionToUpdate.title);

            const updatedData = {
                title: newTitle
            };

            fetch(`http://127.0.0.1:5000/questionnaires/${this.questionnaire.id}/questions/${questionId}`, {
                method: 'PUT',
                headers: {
                'Content-Type': 'application/json'
                },
                body: JSON.stringify(updatedData)
            })
            .then(response => {
                if (response.ok) {
                // Mettre à jour l'interface utilisateur ou afficher un message de confirmation
                console.log('La question a été mise à jour avec succès !');
                // Mettre à jour la liste des questions avec la question modifiée
                questionToUpdate.title = newTitle;
                } else {
                // Gérer les erreurs de mise à jour
                console.error('Erreur lors de la mise à jour de la question :', response.status);
                }
            })
            .catch(error => {
                console.error('Erreur lors de la mise à jour de la question :', error);
            });
        },

        modifierNomQuestionnaire: function() {
            this.$emit('modifierNomQuestionnaire', this.questionnaire.id);
        },

        deleteQuestionnaire: function() {
            this.$emit('deleteQuestionnaire', this.questionnaire.id);
        },

        ajouterQuestion: function() {
            this.$emit('ajouterQuestion', this.questionnaire.id);
        },

        fetchQuestionnaires() {
            if (!this.questionnaire || !this.questionnaire.id) {
                console.error('Aucun questionnaire sélectionné.');
                return;
            }

            fetch(`http://127.0.0.1:5000/questionnaires/${this.questionnaire.id}/questions`)
                .then(response => response.json())
                .then(data => {
                this.questions = data.questions;
                })
                .catch(error => {
                console.error('Erreur lors de la récupération des questions :', error);
                });
        }
    },
    components: {
      Question
    },
    emits: ["modifierNomQuestionnaire","deleteQuestionnaire","ajouterQuestion"]
  };
  </script>
  