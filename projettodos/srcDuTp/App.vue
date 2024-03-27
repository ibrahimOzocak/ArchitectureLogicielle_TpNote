<template>
  <div>
    <h1>MES TÂCHES</h1>
    <ul>
      <TodoItem v-for="item in items"
      :key="item.id"
      :item="item"
      @remove="suppr(item)"
      @edit="edit(item)" />
    </ul>
  </div>
</template>

<script>
import { ref } from 'vue'
import TodoItem from './components/TodoItem.vue';

let data = ref([
        { id: 1, text: 'Faire les courses' },
        { id: 2, text: 'Aller à la poste' },
        { id: 3, text: 'Acheter du pain' }
    ]);

export default {
  data() {
    return {
      items: data
    }
  },
  methods: {
    suppr(item) {
      this.items = this.items.filter(i => i.id !== item.id)
    },   
    edit(item){
      var tache = prompt("Entrer une nouvelle tache", item.text);
      var index = this.items.findIndex(i => i.id===item.id);
      this.items[index].text = tache;
    }
  },
  components: {
    TodoItem
  }
}
</script>

<style>

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 0.5em 0;
}

</style>
