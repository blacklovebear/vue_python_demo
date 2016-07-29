<style scoped>
</style>
<template>
    <tree-select :on-select="onSelect" class="form-control" :tree-data="treeData"></tree-select>

</template>
<script>
  import config from 'config';
  module.exports = {
    props: ['group'],

    data: function () {
      return {
        treeData: [],
      }
    },

    methods: {
      onSelect (item) {
        this.group = item.id;
        this.$dispatch('group-change', this.group);
      },

      loadGroupList: function(){
        var self = this;
        $.ajax({
          url: config.baseUrl + '/groups',
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
      this.loadGroupList();
    }
  }
</script>
