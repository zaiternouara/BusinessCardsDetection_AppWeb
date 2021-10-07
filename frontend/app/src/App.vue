<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title>
      <img src="./assets/Company.png">
      </v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <DataTable/>
         </v-container>
    </v-main>

    <v-footer app> </v-footer>
  </v-app>
</template>

<script>
import DataTable from "./components/DataTable.vue"
export default {
  name: "App",

  components: {
    DataTable
  },
  data: function() {
    return {
      Company: "ALTIUS SERVICES",
    };
  },

};
</script>
<style lang="css">
  img {
     width:18%;
     height:70%;

  }
</style>