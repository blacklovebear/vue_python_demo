
<template>
  <div class="ui search dropdown selection" :class="{ 'active':showMenu }">
    <i class="dropdown icon" @click="onFocus"></i>
    <input class="search" type="text" autocomplete="off" tabindex="0" v-model="searchText" @focus="onFocus"
    />
    <div class="text"></div>
    <div class="menu" :class="{ 'visible':showMenu }" tabindex="-1"  @blur="blurInput">
      <div id="tree"></div>
    </div>
  </div>


  <!-- <button id="expandAll" v-on:click.stop.prevent="expandAll()">Expand All</button> -->
  <!-- <button id="collapseAll" v-on:click.stop.prevent="collapseAll()">Collapse All</button> -->

</template>
<script>
  import config from 'config';
  import TreeView from 'js-treeview';
  import Vue from 'vue';

  module.exports = {

    props: {
      'treeData': {
        type: Array
      },
      'onSelect': {
        type: Function
      }
    },
    data () {
      return {
        showMenu: false,
        searchText: '请选择一个分组',
        tree:null,
      }
    },

    computed:{
      filterData:function(){
        const filter = Vue.filter('filterBy');
        return filter(this.treeData, this.searchText);
      },
    },

    watch:{
      filterData: function(value, oldValue){
        this.buildTree(value);
      }
    },

    methods: {
      resetSelect () {
        this.searchText = ''
      },
      // inputに cursor
      openOptions () {
        this.showMenu = true
      },

      onFocus (){
        this.openOptions();
        this.resetSelect();
      },

      // blurされた時
      blurInput () {
        this.closeOptions();
      },

      closeOptions () {
        this.showMenu = false
      },

      buildTree(valueData) {
        var self = this;
        self.tree = new TreeView(valueData, 'tree');

        self.tree.on('select', function (e) {
            self.searchText = e.data.name;
            self.closeOptions();
            // 回传
            self.onSelect(e.data)
        });
      },

    },

    ready: function(){
      this.buildTree(this.filterData);

    }
  }
</script>
<style scoped>
  @import "/node_modules/js-treeview/dist/treeview.min.css";

  @import '../styles/treeView.css';

  @import '../styles/dropdown.css';


</style>
