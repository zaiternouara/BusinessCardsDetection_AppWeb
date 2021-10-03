<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title>{{ this.Company }}</v-toolbar-title>
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
      Company: "Altius",
    };
  },
};
</script>
