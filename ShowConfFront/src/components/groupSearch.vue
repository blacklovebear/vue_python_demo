<style scoped>
</style>
<template>
    <tree-select :on-select="onSelect" class="form-control" :tree-data="treeData" :search-text="searchText"></tree-select>
</template>
<script>
  import config from 'config';
  import TreeSelect from './treeSelect';

  export default {
    components: {
      'tree-select': TreeSelect,
    },

    props: ['group', 'searchText'],

    data() {
      return {
        treeData: []
      }
    },

    methods: {
      onSelect (item) {
        this.group = item.id;
        this.$dispatch('group-change', item);
      },

      loadGroupList() {
        var self = this;
        $.ajax({
          url: config.baseUrl + '/group/search',
          method: 'GET',
          success(data) {
            self.treeData = data.data;
          },
          error(error) {
            alert(JSON.stringify(error));
          }
        });
      },

    },

    ready() {
      this.loadGroupList();
    }
  }
</script>
