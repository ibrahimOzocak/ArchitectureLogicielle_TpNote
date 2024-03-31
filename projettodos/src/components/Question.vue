<template>
    <li>
      {{ question.title }}
      <input type="button"
        class="btn btn-danger"
        value="MODIFIER" @click="editQuestion">
        <input type="button"
        class="btn btn-danger"
        value="SUPPRIMER" @click="deleteQuestion">
    </li>
  </template>
  
  <script>
  export default {
    props: {
      question: Object // Propriété reçue depuis le composant parent
    },
    methods: {
        editQuestion: function() {
            this.$emit('editQuestion', this.question.id);
        },
        deleteQuestion: function() {
            this.$emit('deleteQuestion', this.question.id);
        }
    },
    emits: ['editQuestion', 'deleteQuestion']
  };
  </script>
  