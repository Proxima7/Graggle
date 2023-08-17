
import axios from 'axios'


const backendURL_Remote = import.meta.env.VITE_BACKENDURL;
const backendURL_Local = "http://localhost:8101"


class RequestHandler {
    constructor() {
        console.log(backendURL_Remote)
        this.backendURL = ""
        this.headers = {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
            }
        if(window.location.hostname == 'localhost'){
            this.backendURL = backendURL_Local
            this.requests_axios = axios.create({
                baseURL: this.backendURL,
                withCredentials: false,
                headers: this.headers,
            });
        } 
        else {
            this.backendURL = "/graggle-backend"
            this.requests_axios = axios.create({
                baseURL: "",
                withCredentials: false,
                headers: this.headers,
            });
        }
        console.log("window.location.hostname: " +  window.location.hostname)
        console.log("this.backendURL: " +  this.backendURL)

         
    }

    // makes a get request on the backend to get the databases. Just invokes the callback.
    get_databases(callback) {
        return this.requests_axios.get(this.backendURL + '/databases').then(callback)
    }

    get_datasets_filtered(callback, filter) {
        return this.requests_axios.post(this.backendURL + '/datasets/filter', {"filter": filter}).then(callback)
    }

    get_dataset_description(callback, callback_error, db, col) {
        return this.requests_axios.get(this.backendURL + '/dataset/description/'+db+'/'+col+'').then(callback).catch(callback_error)
    }

    post_dataset_description(callback, callback_error, body) {
        return this.requests_axios.post(this.backendURL + '/dataset/description', body).then(callback).catch(callback_error)
    }

    get_dataset_comments(callback, db, col) {
        return this.requests_axios.get(this.backendURL + '/dataset/comments/'+db+'/'+col+'').then(callback)
    }    

    get_dataset_document(callback, callback_error, db, col, number, filter, low_resolution) {
        return this.requests_axios.get(this.backendURL + '/dataset/document/'+db+'/'+col+'/'+number+'/'+filter+'?low_resolution='+low_resolution).then(callback).catch(callback_error)
    }



}

const requestHandler = new RequestHandler()

export { requestHandler}
export default requestHandler;