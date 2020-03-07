<template></template>

<script>
export default {
  created() {
      console.log("Created");
      
    this.$store.dispatch("session/DestroyToken");
    this.$router.push({ name: "login" });
  }
};
</script>

<style>
</style>