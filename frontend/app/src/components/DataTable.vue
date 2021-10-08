<template>
  <v-data-table :headers="headers" :items="items" class="elevation-1">
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>Répertoire de contacts</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <MyModal :current="current"  />
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title
              >Voulez-vous vraiment supprimer ce contact ?</v-card-title
            >
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="deleteItemConfirm"
                >SUPPRIMER</v-btn
              >
              <v-btn
                color="blue darken-1"
                text
                @click="dialogDelete = !dialogDelete"
                >ANNULER</v-btn
              >

              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:[`item.actions`]="{ item }">
      <v-icon small @click="editItem(item)" class="mr-2">mdi-pencil</v-icon>
      <v-icon small @click="deleteItem(item)">mdi-delete</v-icon>
    </template>
  </v-data-table>
</template>
<script>
import MyModal from "./MyModal.vue";
import axios from "axios";
import { mapMutations } from 'vuex';
export default {
  data: () => ({
    dialogDelete: false,

    headers: [
      {
        text: "Société",
        align: "start",
        sortable: false,
        value: "company_name",
      },
      {
        text: "Proprietaire",
        value: "propriaitaire",
      },
      { text: "Adresse", value: "adresse" },
      { text: "Email", value: "email" },
      { text: "Fix", value: "fix" },
      { text: "Fax", value: "fax" },
      { text: "Mobile", value: "phone_number" },
      { text: "Site web", value: "website" },
      { text: "Actions", value: "actions" },
    ],
    items: [],
    current: {
      
    },
    dialog: false,
  }),
  components: {
    MyModal,
  },
  mounted: function() {
    axios.get("http://localhost:5000/all").then((result) => {
      this.items = result.data;
    });
  },
  methods: {
    ...mapMutations(["changeValue"]),
    reload() {
      console.log("event catch success");
      this.$forceUpdate();
    },
    editItem(item) {
      //this.changeValue()
      this.$store.commit("changeValue")
      console.log(this.$store.state.dialog)
      this.$emit("open",{"data":this.$store.state.dialog})  
      this.current = item;
      
      console.log(this.current);
    },
    deleteItem(item) {
      console.log("deleted item", item._id);
      this.current = item;
      this.dialogDelete = !this.dialogDelete;
    },
    deleteItemConfirm() {
      axios
        .delete(`http://localhost:5000/remove/${this.current._id.$oid}"`, {
          data: this.current._id.$oid,
        })
        .then((response) => {
          console.log(response);
          this.dialogDelete = !this.dialogDelete;
        })
        .catch((error) => {
          console.log(error);
          this.dialogDelete = !this.dialogDelete;
        });
    },
  },
};
</script>
