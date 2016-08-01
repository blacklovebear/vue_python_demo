<!-- css copy from https://github.com/Semantic-Org/UI-Dropdown/blob/master/dropdown.css -->
<!-- copy from https://www.npmjs.com/package/vue-search-select -->
<template>
  <div class="ui search dropdown selection" :class="{ 'active':showMenu }">
    <i class="dropdown icon" @click="onFocus"></i>
    <input class="search" type="text" autocomplete="off" tabindex="0" v-model="searchText" @focus="onFocus" @blur="blurInput"
           @keydown.up="prevItem"
           @keydown.down="nextItem"
           @keyup.enter="enterItem"
    />
    <div class="text"></div>
    <div class="menu" :class="{ 'visible':showMenu }" tabindex="-1">
      <template v-for="(idx, option) in selectOptions | filterBy searchText">
        <div class="item" :class="{ 'selected': option.selected }" @click="selectItem(option)" @mousedown="mousedownItem">
          {{option.text}}
        </div>
      </template>
    </div>
  </div>
</template>

<script>
  import Vue from 'vue'
  export default {
    props: {
      'selectOptions': {
        type: Array
      },
      'onSelect': {
        type: Function
      }
    },
    data () {
      return {
        showMenu: false,
        searchText: '',
        mousedownState: false
      }
    },
    computed: {
      filteredOptions () {
        const filter = Vue.filter('filterBy')
        return filter(this.selectOptions, this.searchText)
      }
    },
    watch: {
      'selectOptions': function (val, oldVal) {
        var selectedItem = val.find(item => {
          return item.selected === true
        })
        if (selectedItem) {
          this.selectItem(selectedItem)
        } else {
          this.selectItem({})
        }
      },

    },
    methods: {
      resetSelect () {
        this.searchText = ''
      },
      // inputに cursor
      openOptions () {
        this.showMenu = true
        this.mousedownState = false
      },

      onFocus (){
        this.openOptions();
        this.resetSelect();
      },

      // blurされた時
      blurInput () {
        if (!this.mousedownState) {
          this.closeOptions();
          // this.enterItem();

          let selectedItem = this.filteredOptions.find(item => {
            return item.selected === true
          })
          this.searchText = selectedItem.text


        }
      },
      closeOptions () {
        this.showMenu = false
      },
      // up arrow key
      prevItem () {
        let selectedItemIndex = this.filteredOptions.findIndex(item => {
          return item.selected === true
        })
        if (selectedItemIndex === -1) {
          this.filteredOptions[0].selected = true
        } else if (selectedItemIndex === 0) {
          // nothing todo
        } else {
          this.filteredOptions[selectedItemIndex].selected = false
          this.filteredOptions[selectedItemIndex - 1].selected = true
        }
      },
      // down arrow key
      nextItem () {
        let selectedItemIndex = this.filteredOptions.findIndex(item => {
          return item.selected === true
        })
        if (selectedItemIndex === -1) {
          this.filteredOptions[0].selected = true
        } else if (selectedItemIndex === this.filteredOptions.length - 1) {
          // nothing todo
        } else {
          this.filteredOptions[selectedItemIndex].selected = false
          this.filteredOptions[selectedItemIndex + 1].selected = true
        }
      },
      enterItem () {
        // selected = trueのitemをセット
        let selectedItem = this.filteredOptions.find(item => {
          return item.selected === true
        })
        this.selectItem(selectedItem)
      },
      mousedownItem () {
        this.mousedownState = true
      },

      changeSelected(option) {
        _.forEach(this.selectOptions, function(value){
          value.selected = false;
        })
        option.selected = true;
      },

      selectItem (option) {
        this.searchText = option.text
        this.closeOptions()
        this.onSelect(option);

        this.changeSelected(option);
      }
    }
  }
</script>

<style scoped>
  @import '../styles/dropdown.css';
</style>

