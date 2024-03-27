<template>
    <li>
        {{ item.text }}
        <input type="button"
        class="btn btn-danger"
        value="SUPPRIMER" @click="remove">
        <input type="button"
        class="btn btn-danger"
        value="EDIT" @click="edit">
    </li>
</template>
  
<script>
export default {
    props: {
        item: Object
    },
    methods: {
        remove: function() {
            this.$emit('remove', this.item.id);
        },
        edit: function() {
            this.$emit('edit', this.item.id);
        }
    },
    emits: ['remove', 'edit']
}
</script>
