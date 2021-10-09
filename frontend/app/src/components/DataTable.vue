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
        <v-dialog v-model="dialogUpdate" persistent max-width="600px">

        <v-card>
          <v-card-title>
            <span class="text-h5">Modifier un contact</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="Société *"
                    required
                    v-model="current.company_name"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="Fix *"
                    required
                    v-model="current.fix"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="Fax *"
                    required
                    v-model="current.fax"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    label="Mobile *"
                    required
                    v-model="current.phone_number"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    label="Email*"
                    required
                    v-model="current.email"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    label="Propriétaire de la carte *"
                    required
                    v-model="current.propriaitaire"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    label="Site web *"
                    required
                    v-model="current.website"
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-textarea
                    label="Adresse *"
                    required
                    v-model="current.adresse"
                  >
                  </v-textarea>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-file-input
                    chips
                    accept="image/*"
                    label="Insérer la carte de visite ici"
                    v-model="current.filepath"
                  ></v-file-input>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>

            <v-btn color="blue darken-1" text @click="check">
              DETÉCTER
            </v-btn>

            <v-btn color="blue darken-1" text @click="UpdateItem">
              MODIFIER
            </v-btn>

            <v-btn color="blue darken-1" text @click="dialogUpdate = !dialogUpdate">
              FERMER
            </v-btn>
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
    dialogUpdate:false,
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
        company_name: "",
        phone_number: "",
        fax: "",
        email: "",
        website: "",
        adresse: "",
        fix: "",
        propriaitaire: "",
        filepath: "",
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
       console.log(this.$store.state.dialog)
      this.current = item;
      this.dialogUpdate = !this.dialogUpdate;

      //this.$emit("open",{"data":this.$store.state.dialog})
      //this.current = item;

      //console.log(this.current);


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
    check() {
       let data = new FormData()
       data.append("file",this.current.filepath)
      console.log(this.current.filepath);
      axios
        .post(
          "http://localhost:5000/upload", data, {
            headers: {
               'Content-Type': `multipart/form-data`
            }
          }
        )
        .then((response) => {
          console.log(response);
          this.current = {
            company_name: response.data['Company'],
            phone_number: response.data['Mob'],
            fax: response.data['Fax'],
            email: response.data['Email'],
            website: response.data['Website'],
            adresse: response.data['Address'],
            fix: response.data['Fix'],
            propriaitaire: response.data['Name'],
            filepath: "",
          };
        })
        .catch((error) => {
          console.log(error);
        });
    },

    UpdateItem() {

      axios
        .put(`http://localhost:5000/update/${this.current._id.$oid}`, {
          company_name: this.current.company_name,
          phone_number: this.current.phone_number,
          fax: this.current.fax,
          email: this.current.email,
          website: this.current.website,
          adresse: this.current.adresse,
          fix: this.current.fix,
          propriaitaire: this.current.propriaitaire,
        })
        .then((response) => {
          /**console.log(response);**/
          console.log(response)
          this.current = {
            company_name: response.data['Company'],
            phone_number: response.data['Mob'],
            fax: response.data['Fax'],
            email: response.data['Email'],
            website: response.data['Website'],
            adresse: response.data['Address'],
            fix: response.data['Fix'],
            propriaitaire: response.data['Name'],
            filepath: "",
            };
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>
