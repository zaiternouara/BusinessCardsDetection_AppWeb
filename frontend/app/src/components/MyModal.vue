<template>
  <div>
    <v-row justify="center">
      <v-dialog v-model="dialog" persistent max-width="600px">
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            color="primary"
            fab
            dark
            v-bind="attrs"
            v-on="on"
            @click="reset"
          >
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </template>
        <v-card>
          <v-card-title>
            <span class="text-h5">{{ title }}</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="Nom Company"
                    required
                    v-model="current.company_name"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="Fix"
                    required
                    v-model="current.fix"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-text-field
                    label="Fax"
                    required
                    v-model="current.fax"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    label="Mobile*"
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
                    label="Propriétaire de la carte"
                    required
                    v-model="current.proprio"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    label="Website"
                    required
                    v-model="current.website"
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-textarea
                    label="Adresse "
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
                    label="File input"
                    v-model="current.filepath"
                  ></v-file-input>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="close">
              Close
            </v-btn>
            <v-btn color="blue darken-1" text @click="click">
              Save
            </v-btn>
            <v-btn color="blue darken-1" text @click="check">
              check
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </div>
</template>
<script>
import axios from "axios";
import { mapState } from "vuex";
export default {
  name: "MyModal",
  props: {
    title: {
      type: String,
      default: "Ajouter Une Company",
    },
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
  },

  computed: {
    ...mapState({
      dialog: (state) => state.dialog,
    }),
  },

  methods: {
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
    reset() {
      this.current = {
        company_name: "",
        phone_number: "",
        fax: "",
        email: "",
        website: "",
        adresse: "",
        fix: "",
        propriaitaire: "",
        filepath: "",
      };
    },
    close() {
      this.$store.commit("changeValue");
    },
    click() {
      this.dialog = !this.dialog;
      console.log("this me ", this.fax);
      axios
        .post("http://localhost:5000/add", {
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

<style></style>
