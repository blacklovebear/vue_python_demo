<style scoped>

</style>
<template>
<p></p>
  <div class="row">
    <div class="col-md-4">
      <tree-select :select-options="[]"
                    :on-select="test" class="form-control" :tree-data="treeData"></tree-select>

    </div>
  </div>
</template>
<script>
  import config from 'config';

  module.exports = {
    data: function(){
      return {
        treeData: [
                      { name: 'wewewe', children: [] },
                      { name: 'tewerwer', expanded: true, children: [
                              { name: '232323', children: [] },
                              { name: 'rtyryr', children: [] }
                          ]
                      }
                  ],
      }
    },

    methods: {
      test() {
        alert(111);
      }

    },

    ready: function () {

    }


  }
</script>
