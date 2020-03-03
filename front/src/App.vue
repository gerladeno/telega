<template>
  <div id="app">
    <component :is="layout">
      <router-view />
    </component>
  </div>
</template>

<script>
import EmptyLayout from "@/layouts/EmptyLayout";

export default {
  name: "App",
  computed: {
    layout() {
      return this.$route.meta.layout;
    }
  },
  data() {
    return {};
  },
  mounted() {},
  components: {
    EmptyLayout
  }
};
</script>

<style lang = "scss">
@import "~materialize-css/dist/css/materialize.css";
</style>
