<style scoped>
</style>
<template>
    <tree-select :on-select="onSelect" class="form-control" :tree-data="treeData" :search-text="searchText"></tree-select>

</template>
<script>
  import config from 'config';
  module.exports = {
    props: ['parentSection', 'searchText'],

    data: function () {
      return {
        treeData: []
      }
    },

    methods: {
      onSelect (item) {
        this.parentSection = item.id;
        this.$dispatch('section-change', this.parentSection);
      },

      loadSectionList: function(){
        var self = this;
        $.ajax({
          url: config.baseUrl + '/group/search?only_section=1',
          method: 'GET',
          success: function(data){
            self.treeData = data.data;
          },
          error: function(error){
            alert(JSON.stringify(error));
          }
        });
      },

    },

    ready: function(){
      this.loadSectionList();
    }
  }
</script>
