import { get, put, post, del } from './modules'
export default {

getBookedFlats() {
   return get("flats/");
},

getAllFlats() {
   return get("flats/allflats/");
},

getByOrder() {
   return get("flats/byorder/");
},

newBooking(item) {
   return post("flats/", item)
},

delBooking(item) {
   return del(`flats/${item}/`, item)
},

editBooking(item, data) {
   return put(`flats/${item}/`, data)
},

availableBookings(item) {
   return get(`flats/available_flats/?${item}`, )
},

sendPDF(item) {
   return post("flats/send_pdf/", item)
},
}