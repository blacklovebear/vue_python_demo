<style scoped>
    @import '../styles/common.css';
    #menu-toggle{
        position: absolute;
        top: 10px;
    }
</style>
<template>

  <div id="wrapper">

        <div id="sidebar-wrapper">
            <ul class="sidebar-nav">
                <li class="sidebar-brand">
                    <a href="#">
                        配置管理
                    </a>
                </li>
                <li>
                    <a v-link="{name: 'index'}">配置文件列表</a>
                </li>
                <li>
                    <a v-link="{name: 'groupList'}">分组列表</a>
                </li>
                <li>
                    <a v-link="{name: 'confInfo'}">添加配置文件</a>
                </li>
                <li>
                    <a v-link="{name: 'groupInfo'}">增加分组</a>
                </li>

            </ul>
        </div>

        <!-- Page Content -->
        <div id="page-content-wrapper">
          <a href="#menu-toggle" id="menu-toggle" v-on:click.stop.prevent="toggleClass()">侧边栏显隐</a>
          <router-view></router-view>

        </div>

    </div>


</template>
<script>
  module.exports = {
      data: function() {
          return {

          }
      },
      ready: function() {

      },
      beforeDestroy: function() {

      },
      methods: {
        toggleClass: function(){
          $("#wrapper").toggleClass("toggled");
        }

      }
  }
</script>
