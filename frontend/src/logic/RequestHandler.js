
import axios from 'axios'


const backendURL_Remote = import.meta.env.VITE_BACKENDURL;
const backendURL_Local = "http://localhost:8101"


class RequestHandler {
    constructor() {
        console.log(backendURL_Remote)
        if(window.location.hostname == 'localhost'){
            this.backendURL = backendURL_Local
        } else {
            this.backendURL = backendURL_Remote
        }
        console.log("window.location.hostname: " +  window.location.hostname)
        console.log("this.backendURL: " +  this.backendURL)

        this.requests_axios = axios.create({
            baseURL: this.backendURL,
            withCredentials: false,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
              },
          }); 
    }

    // makes a get request on the backend to get the databases. Just invokes the callback.
    get_databases(callback) {
        return this.requests_axios.get(this.backendURL + '/get/databases').then(callback)
    }

    get_database(callback, database_name) {
        return this.requests_axios.post(this.backendURL + '/post/database', { "database_name": database_name}).then(callback)
    }

    get_dataset_description(callback, callback_error, db, col) {
        return this.requests_axios.get(this.backendURL + '/dataset/description/'+db+'/'+col+'').then(callback).catch(callback_error)
    }

    get_dataset_comments(callback, db, col) {
        return this.requests_axios.get(this.backendURL + '/dataset/comments/'+db+'/'+col+'').then(callback)
    }

    get_datasets(callback, filter) {
        return this.requests_axios.post(this.backendURL + '/datasets/filter', {"filter": filter}).then(callback)
    }

    post_dataset_description(callback, callback_error, body) {
        return this.requests_axios.post(this.backendURL + '/dataset/description', body).then(callback).catch(callback_error)
    }

    get_dataset(callback, callback_error, db, col, number, filter, low_resolution) {
        return this.requests_axios.get(this.backendURL + '/data/'+db+'/'+col+'/'+number+'/'+filter+'?low_resolution='+low_resolution).then(callback).catch(callback_error)
    }

    get_dataset_documents(callback, database_name, dataset_name) {
        return this.requests_axios.post(this.backendURL + '/post/dataset/documents', { 
            "database_name": database_name, 
            "dataset_name": dataset_name}).then(callback)
    }

}

const requestHandler = new RequestHandler()

export { requestHandler}
export default requestHandler;