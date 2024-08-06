<template>
  <div class="mainContainer">
    <!-- head -->
    <div>
      <h1 class="cta">Rent Now your flat with us</h1>
    </div>
    <div class="wallpaper-container">
      <img :src="wallpaper" alt="wallpaper" class="wallpaper-image" />
    </div>
    <!-- form -->
    <v-container class="containerInput d-flex justify-center align-center">
      <v-card
        class="pa-5 d-flex justify-center align-center"
        width="800"
        elevation="2"
        ><v-container>
          <v-row wrap>
            <v-col xs="12" sm="12" md="5">
              <v-date-input
                elevation="24"
                label="Date Checkin"
                v-model="dateCheckin"
              ></v-date-input>
            </v-col>
            <v-col xs="12" sm="12" md="5">
              <v-date-input
                elevation="24"
                label="Date Checkout"
                v-model="dateCheckout"
              ></v-date-input>
            </v-col>

            <v-col xs="12" sm="2" md="2">
              <v-btn @click="availableBookings" variant="tonal" color="blue">
                Consult
              </v-btn>
            </v-col>
          </v-row>
        </v-container></v-card
      >
    </v-container>
    <!-- body -->
    <v-container>
      <v-row>
        <v-card class="mx-auto my-8" elevation="2" max-width="344">
          <img :src="flat1" class="cardImage" />
          <v-card-item>
            <v-card-title> FLAT 1 </v-card-title>
          </v-card-item>

          <v-card-text>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua.
          </v-card-text>
        </v-card>
        <v-card class="mx-auto my-8" elevation="2" max-width="344">
          <img :src="flat2" class="cardImage" />
          <v-card-item>
            <v-card-title> FLAT 2 </v-card-title>
          </v-card-item>

          <v-card-text>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua.
          </v-card-text>
        </v-card>
        <v-card class="mx-auto my-8" elevation="2" max-width="344">
          <img :src="flat3" class="cardImage" />
          <v-card-item>
            <v-card-title> FLAT 3 </v-card-title>
          </v-card-item>

          <v-card-text>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua.
          </v-card-text>
        </v-card>
      </v-row>
    </v-container>
    <!-- flat available dialog -->
    <v-dialog v-model="dialog" width="700" class="overflow-y-auto">
      <v-card
        width="auto"
        prepend-icon="mdi-checkbox-marked-outline"
        title="Flats available"
        class="pa-5"
        elevation="10"
      >
        <template v-slot:actions>
          <v-row class="justify-end">
            <v-btn
              text="Save PDF"
              @click="(pdfDialog = true), (dialog = false)"
            ></v-btn>
            <v-btn text="Cancel" @click="dialog = false"></v-btn>
            <v-btn
              @click="saveEditedBooking"
              variant="tonal"
              disable
              :disabled="true"
            >
              Choose
            </v-btn>
          </v-row>
        </template>
        <v-card
          style="
            max-height: 500px;
            overflow-y: auto;
            color: transparent;
            padding: none;
          "
        >
          <v-card
            elevation="2"
            style="margin-top: 10px"
            v-for="item in availableFlats"
            :key="item"
          >
            <v-row>
              <v-col cols="12" sm="5">
                <img :src="flat1" class="availableImage"
              /></v-col>
              <!-- {{ availableFlats }} -->
              <v-col cols="12" sm="7">
                <v-card-item>
                  <v-card-title> {{ item.nome }} </v-card-title>
                </v-card-item>

                <v-card-text>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
                  do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                </v-card-text></v-col
              >
            </v-row>
          </v-card>
        </v-card>
      </v-card>
    </v-dialog>

    <v-dialog v-model="pdfDialog" width="700">
      <v-card
        width="auto"
        prepend-icon="mdi-email-outline"
        title="Write Your Email"
        class="pa-5"
        elevation="10"
      >
        <template v-slot:actions>
          <v-row class="justify-end">
            <v-btn
              text="Cancel"
              @click="(pdfDialog = false), (dialog = true)"
            ></v-btn>
            <v-btn @click="sendthePdf" variant="tonal"> Send </v-btn>
          </v-row>
        </template>

        <v-text-field
          hide-details="auto"
          label="E-mail"
          v-model="email"
        ></v-text-field>
      </v-card>
    </v-dialog>
  </div>
</template>
 
 <script>
import wallpaper from "@/assets/wallpaper.jpg";
import flat1 from "@/assets/flat1.jpg";
import flat2 from "@/assets/flat2.jpg";
import flat3 from "@/assets/flat3.jpg";

import api from "@/api/api";
import { VDateInput } from "vuetify/labs/VDateInput";
export default {
  components: {
    VDateInput,
  },

  data() {
    return {
      wallpaper,
      flat1,
      flat2,
      flat3,
      dialog: false,
      pdfDialog: false,
      dateCheckin: null,
      dateCheckout: null,
      flatIdNameMap: {},
      availableFlats: [],
      availableFlatIds: [],
      email: null,
    };
  },
  mounted() {},
  methods: {
    initialize() {
      this.getFlats();
    },
    async getFlats() {
      try {
        const allFlatsResponse = await api.getAllFlats();
        this.flats = allFlatsResponse.data;
        this.flatIdNameMap = this.flats.reduce((map, flat) => {
          map[flat.id] = flat.nome;
          return map;
        }, {});
      } catch (error) {
        console.log(error);
      }
    },
    getFlatName(flatId) {
      return this.flatIdNameMap[flatId] || "Unknown Flat";
    },
    formatDate(date) {
      if (!date) return "";
      return date.toISOString().split("T")[0];
    },

    async availableBookings() {
      if (!this.dateCheckin || !this.dateCheckout) {
        alert("All fields must be filled out.");
        return;
      }

      const checkin = this.formatDate(this.dateCheckin);
      const checkout = this.formatDate(this.dateCheckout);

      try {
        const item = `checkin=${checkin}&checkout=${checkout}`;
        const availableFlatsResponse = await api.availableBookings(item);
        this.availableFlats = availableFlatsResponse.data;
        this.availableFlatIds = this.availableFlats.map((flat) => flat.id);
        this.dialog = true;
      } catch (error) {
        console.log(error);
      }
    },
    async sendthePdf() {
      if (!this.email) {
        alert("Email must be provided");
        return;
      }

      const item = {
        email: this.email,
        flatIds: this.availableFlatIds,
      };

      try {
        await api.sendPDF(item);
        alert("Enviado");
        this.dialog = false;
        this.pdfDialog = false;
        (this.dateCheckin = null),
          (this.dateCheckout = null),
          (this.email = null);
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>
 

<style scoped>
.wallpaper-image {
  width: 100%;
  height: 500px;
  filter: blur(2px);
  filter: brightness(60%);
  object-fit: cover;
}
.wallpaper-container {
  position: relative;
  width: 100%;
  height: 500px;
}
.mainContainer {
  margin: 0;
  padding: 0;
  height: 100vh;
  position: relative;
}
.cta {
  position: absolute;
  top: 33%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  z-index: 1;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
  font-size: 55px;
  font-family: "Times New Roman", Times, serif;
  text-align: center;
}
.containerInput {
  margin-top: -100px;
}

.cardImage {
  display: block;
  margin: 0;
  height: 300px;
  width: 320px;
}

.availableImage {
  display: block;
  margin: none;
  height: 230px;
  width: 265px;
}
@media (max-width: 600px) {
  .wallpaper-image,
  .wallpaper-container {
    height: 300px;
  }
  .cta {
    font-size: 30px;
    top: 20%;
  }
  .containerInput {
    margin-top: -50px;
  }
}
</style>