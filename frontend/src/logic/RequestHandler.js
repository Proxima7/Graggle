
import axios from 'axios'

const backendURL = "http://localhost:8101"

const requests_axios = axios.create({
    baseURL: backendURL,
    //headers: {'Accept': 'application/json', 'Content-Type': 'application/json'},
    withCredentials: false,
    headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
      },
    //timeout: 20000
  });

 


class RequestHandler {
    constructor() {
        this.backendURL = backendURL
    }

    // makes a get request on the backend to get the databases. Just invokes the callback.
    get_databases(callback) {
        return requests_axios.get(this.backendURL + '/get/databases').then(callback)
    }

    get_database(callback, database_name) {
        return requests_axios.post(this.backendURL + '/post/database', { "database_name": database_name}).then(callback)
    }

    get_dataset_description(callback, callback_error, db, col) {
        return requests_axios.get(this.backendURL + '/dataset/description/'+db+'/'+col+'').then(callback).catch(callback_error)
    }

    get_dataset_comments(callback, db, col) {
        return requests_axios.get(this.backendURL + '/dataset/comments/'+db+'/'+col+'').then(callback)
    }

    get_datasets(callback, filter) {
        return requests_axios.post(this.backendURL + '/datasets/filter', {"filter": filter}).then(callback)
    }

    post_dataset_description(callback, callback_error, body) {
        return requests_axios.post(this.backendURL + '/dataset/description', body).then(callback).catch(callback_error)
    }

    get_dataset(callback, callback_error, db, col, number, filter) {
        return requests_axios.get(this.backendURL + '/data/'+db+'/'+col+'/'+number+'/'+filter).then(callback).catch(callback_error)
    }

    get_dataset_documents(callback, database_name, dataset_name) {
        return requests_axios.post(this.backendURL + '/post/dataset/documents', { 
            "database_name": database_name, 
            "dataset_name": dataset_name}).then(callback)
    }

}

const requestHandler = new RequestHandler()

export { requestHandler, requests_axios, backendURL }
export default requestHandler;