<template>
  <h1>{{message}}</h1>
</template>

<script>
import axios from 'axios'
export default {
    name: "master",
  data() {
      return {
          message: ""
      };
  },
    methods:{
        load: function(){
            axios.get("/say")
            .then(response => this.message = response)
            .catch(error => this.message = error)
        }
    },
    created(){
        this.load()
    }
}
</script>

<style>

</style>