<template>
  <v-responsive class="align-centerfill-height mx-auto" max-width="900">
    <v-container>
      <v-card class="pa-5" elevation="2">
        <v-container class="pt-8">
          <v-row>
            <v-select
              label="Choose Flat"
              v-model="selFlat"
              :items="flats"
              item-value="id"
              item-title="name"
              variant="underlined"
            >
            </v-select>
            <v-date-input
              elevation="24"
              label="Date Checkin"
              v-model="dateCheckin"
            ></v-date-input>
            <v-date-input
              elevation="24"
              label="Date Checkout"
              v-model="dateCheckout"
            ></v-date-input>
            <v-col>
              <v-btn @click="saveBooking" variant="tonal" color="blue">
                Save
              </v-btn></v-col
            >
          </v-row>
        </v-container>
      </v-card>

      <v-table>
        <thead>
          <tr>
            <th class="text-left">Flat</th>
            <th class="text-left">Id Booking</th>
            <th class="text-left">Checkin</th>
            <th class="text-left">Checkout</th>
            <th class="text-left">Order</th>
            <th class="text-left">Previus</th>
            <th class="text-left">
              Actions
              <v-icon class="pl-10" @click="Order">mdi-tune</v-icon>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in bookedFlats" :key="item">
            <td>{{ getFlatName(item.flat) }}</td>
            <td>{{ item.id }}</td>
            <td>{{ item.checkin }}</td>
            <td>{{ item.checkout }}</td>
            <td>{{ item.ordem }}</td>
            <td>
              {{
                item.ordem === 1
                  ? "-"
                  : bookedFlats.filter(
                      (current) =>
                        current.flat === item.flat &&
                        current.ordem === item.ordem - 1
                    )[0].id
              }}
            </td>
            <td>
              <v-btn
                variant="tonal"
                color="red"
                @click="deleteBooking(item.id)"
                class="mr-2"
                >Delete</v-btn
              >
              <v-btn variant="tonal" color="green" @click="openEditDialog(item)"
                >Edit</v-btn
              >
            </td>
          </tr>
        </tbody>
      </v-table>
      <v-dialog v-model="dialog" width="500">
        <v-card
          width="auto"
          prepend-icon="mdi-update"
          title="Edit Booking"
          class="pa-5"
        >
          <template v-slot:actions>
            <v-btn
              class="ms-auto"
              text="Cancel"
              @click="dialog = false"
            ></v-btn>
            <v-btn @click="saveEditedBooking" variant="tonal"> Save </v-btn>
          </template>
          <v-col class="pa-3">
            <v-select
              label="Choose Flat"
              v-model="selFlat"
              :items="flats"
              item-value="id"
              item-title="name"
              variant="underlined"
            >
            </v-select
          ></v-col>
          <v-col class="pa-3">
            <v-date-input
              elevation="24"
              label="Date Checkin"
              v-model="dateCheckin"
            ></v-date-input
          ></v-col>
          <v-col class="pa-3"
            ><v-date-input
              elevation="24"
              label="Date Checkout"
              v-model="dateCheckout"
            ></v-date-input
          ></v-col> </v-card
      ></v-dialog>
    </v-container>
  </v-responsive>
</template>
<script>
import api from "@/api/api";
import { VDateInput } from "vuetify/labs/VDateInput";
export default {
  components: {
    VDateInput,
  },
  data() {
    return {
      flats: [],
      bookedFlats: [],
      selFlat: null,
      dateCheckin: null,
      dateCheckout: null,
      flatIdNameMap: {},
      dialog: false,
      currentBookingId: null,
      changeOrder: false,
    };
  },

  mounted() {
    this.initialize();
  },
  computed: {},

  methods: {
    getFlatName(flatId) {
      return this.flatIdNameMap[flatId] || "Unknown Flat";
    },
    formatDate(date) {
      if (!date) return "";
      return date.toISOString().split("T")[0];
    },
    initialize() {
      this.getBookins();
      this.getFlats();
    },

    async getFlats() {
      try {
        const allFlatsResponse = await api.getAllFlats();
        this.flats = allFlatsResponse.data;

        this.flatIdNameMap = this.flats.reduce((map, flat) => {
          map[flat.id] = flat.name;
          return map;
        }, {});
      } catch (error) {
        console.log(error);
      }
    },

    async getBookins() {
      try {
        const bookedFlatsResponse = await api.getBookedFlats();
        this.bookedFlats = bookedFlatsResponse.data;
      } catch (error) {
        console.log(error);
      }
    },

    Order() {
      this.changeOrder = !this.changeOrder;
      this.changeOrder ? this.getByOrder() : this.getBookins();
    },

    async getByOrder() {
      try {
        const bookedFlatsResponse = await api.getByOrder();
        this.bookedFlats = bookedFlatsResponse.data;
      } catch (err) {
        console.error("Erro ao carregar dados:", err);
      }
    },

    async saveBooking() {
      if (!this.selFlat || !this.dateCheckin || !this.dateCheckout) {
        alert("All fields must be filled in");
        return;
      }
      const bookingData = {
        flat: this.selFlat,
        checkin: this.formatDate(this.dateCheckin),
        checkout: this.formatDate(this.dateCheckout),
      };

      try {
        await api.newBooking(bookingData);
        console.log("Reservation created successfully");
        await this.getBookins();
        this.selFlat = null;
        this.dateCheckin = null;
        this.dateCheckout = null;
      } catch (err) {
        console.error("Error creating reservation", err);
        alert(err);
      }
    },
    openEditDialog(item) {
      this.currentBookingId = item.id;
      this.selFlat = item.flat;
      this.dateCheckin = new Date(item.checkin);
      this.dateCheckout = new Date(item.checkout);
      this.dialog = true;
      console.log(this.currentBookingId);
    },
    async saveEditedBooking() {
      console.log(this.currentBookingId);

      if (!this.selFlat || !this.dateCheckin || !this.dateCheckout) {
        alert("All fields must be completed.");
        return;
      }
      const bookingData = {
        flat: this.selFlat,
        checkin: this.formatDate(this.dateCheckin),
        checkout: this.formatDate(this.dateCheckout),
      };

      try {
        await api.editBooking(this.currentBookingId, bookingData);
        alert("Reservation edited successfully.");
        await this.getBookins();
        this.dialog = false;
        this.selFlat = null;
        this.dateCheckin = null;
        this.dateCheckout = null;
      } catch (err) {
        alert("Error editing reservation");
      }
    },

    async deleteBooking(bookingId) {
      if (!bookingId) {
        console.error("Reservation ID not provided");
        return;
      }

      try {
        await api.delBooking(bookingId);
        console.log("Reservation deleted successfully!");
        await this.getBookins();
      } catch (err) {
        console.error("Error deleting reservation.", err);
        alert("Error deleting reservation");
      }
    },
  },
};
</script>

