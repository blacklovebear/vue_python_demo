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
            Configure Display
        </a>
      </li>
      <li>
        <a v-link="{name: 'index'}">Configure List</a>
      </li>
      <li>
        <a v-link="{name: 'groupList'}">Group List</a>
      </li>

    </ul>
  </div>

  <div id="page-content-wrapper">
    <a href="#menu-toggle" id="menu-toggle" v-on:click.stop.prevent="toggleClass()">Sidebar toggle</a>
    <router-view></router-view>
  </div>
</div>
</template>

<script>
  export default {
    methods: {
      toggleClass: function(){
        $("#wrapper").toggleClass("toggled");
      }

    }
  }
</script>
