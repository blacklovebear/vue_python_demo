<style scoped>
</style>
<template>
    <select-search class="form-control"
      :select-options="selectOptions"
      :on-select="selectedItem"></select-search>

</template>
<script>
  import config from 'config';
  module.exports = {
    props: ['group'],

    data: function () {
      return {
        selectOptions: [],
      }
    },

    methods: {
      selectedItem (item) {
        this.group = item.value;
        this.$dispatch('group-change', this.group);
        this.searchText = '';
      },

      setSelectOptions: function(responseData){
        var self = this;
        var tempList = _.map(responseData, function(x){
          return {value: x.id, text: x.name, selected: x.id === self.group ? true : false}
        })

        self.selectOptions = _.concat([{value:0, text:'选择分组', selected: 0 === self.group ? true : false}], tempList);
      },

      loadGroupList: function(){
        var self = this;
        $.ajax({
          url: config.baseUrl + '/groups',
          method: 'GET',
          success: function(data){
            self.groupList = data.data;
            self.setSelectOptions(data.data);

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
