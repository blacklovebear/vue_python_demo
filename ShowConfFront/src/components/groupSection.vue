<style scoped>
</style>
<template>
    <select-search :on-select="onSelect" class="form-control" :select-options="selectOptions" :search-text="searchText"></select-search>
</template>
<script>
  import config from 'config';
  import SelectSearch from './selectSearch';

  export default {
    components: {
      'select-search': SelectSearch,
    },

    props: ['parentSection', 'searchText'],

    data() {
      return {
        selectOptions: []
      }
    },

    methods: {
      onSelect(item) {
        this.parentSection = item.id;
        this.$dispatch('section-change', this.parentSection);
      },

      loadSectionList() {
        let self = this;
        $.ajax({
          url: config.baseUrl + '/group/section',
          method: 'GET',
          success(data) {
            self.selectOptions = data.data;
          },
          error(error) {
            alert(JSON.stringify(error));
          }
        });
      },
    },

    ready() {
      this.loadSectionList();
    }
  }
</script>
