<style scoped>
</style>
<template>
    <select-search :on-select="onSelect" class="form-control" :select-options="selectOptions" :search-text="searchText"></select-search>
</template>
<script>
  import config from 'config';
  module.exports = {
    props: ['parentSection', 'searchText'],

    data: function () {
      return {
        selectOptions: []
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
          url: config.baseUrl + '/group/section',
          method: 'GET',
          success: function(data){
            self.selectOptions = data.data;
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
