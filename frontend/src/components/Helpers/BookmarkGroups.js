
import requestHandler from "../../logic/RequestHandler"
import { useGeneralStore } from '@/stores/general'

export class BookmarkGroups {

    static local_storace_name = 'bookmarkgroups'

    static async _readBookmarkGroups( ){
        const gstore = useGeneralStore()
        if(gstore.global_storage){
            var global_groups = []
            const bookmark_group_callback = function(resp){
                global_groups = resp.data.groups
              }
            await requestHandler.get_bookmark_groups(bookmark_group_callback)
            return global_groups
        } else {
            const groups = JSON.parse(localStorage.getItem(BookmarkGroups.local_storace_name)) || [];
            return groups
        }        
    }

    static async _writeBookmarkGroup(groups){
        const gstore = useGeneralStore()
        if(gstore.global_storage){
            const bookmark_group_callback = function(resp){
                console.log(resp)
              }
            await requestHandler.post_bookmark_groups(bookmark_group_callback, {"groups": groups})
        } else {
            localStorage.setItem(BookmarkGroups.local_storace_name, JSON.stringify(groups));
        }  
        
    }


    static async _createBookmarkGroup(name, db, col){
        let groups = await this._readBookmarkGroups()
        groups.push({"name": name, "datasets": [{"db": db, "col": col }]})
        await this._writeBookmarkGroup(groups)
    }

    static adjustCounter(store){
        store.amount_bookmark_groups = store.amount_bookmark_groups+1       
    }


    static async _add2BookmarkGroup(name, db, col){
        let groups = await this._readBookmarkGroups()
        for(let i=0; i<groups.length; i++){
            if(groups[i].name == name){
                groups[i].datasets.push({"db": db, "col": col })
            }
        }
        await this._writeBookmarkGroup(groups)
    }

    static async _removeBookmarkGroup(name, db, col){
        let groups = await this._readBookmarkGroups()
        for(let i=0; i<groups.length; i++){
            if(groups[i].name == name){
                let remove_dataset_index=-1
                for(let ds=0; ds<groups[i].datasets.length; ds++){
                    if(db==groups[i].datasets[ds].db && col==groups[i].datasets[ds].col){
                        remove_dataset_index = ds
                    }
                }
                if(remove_dataset_index!=-1){
                    groups[i].datasets.splice(remove_dataset_index)

                    if(groups[i].datasets.length==0){
                        groups.splice(i) 
                    }
                }
            }
        }
        await this._writeBookmarkGroup(groups)
    }
    
    static async addBookmarkGroup(name, db, col, store){
        await this._add2BookmarkGroup(name, db, col)
        this.adjustCounter(store)
    }

    static async removeBookmarkGroup(name, db, col, store){
        await this. _removeBookmarkGroup(name, db, col)
        this.adjustCounter(store)
    }
    

    static async setBookmarkGroup(name, db, col, store){
        await this._createBookmarkGroup(name, db, col)
        this.adjustCounter(store)
    }

    static async getBookmarkGroups(db, col){
        let bookmarkgroups = await this._readBookmarkGroups()
        return bookmarkgroups

        // optional
        // remove me from the list
        if(db!="" && col!=""){            
            let inside_index = -1
            for(let i=0; i<bookmarkgroups.length; i++){
                for(let ds=0; ds<bookmarkgroups[i].datasets.length; ds++){
                    if(db==bookmarkgroups[i].datasets[ds].db && col==bookmarkgroups[i].datasets[ds].col){
                        inside_index=i
                    }
                }
            }
            if(inside_index!=-1){
                bookmarkgroups.splice(inside_index)
            }
        }
        return bookmarkgroups
        
    }

}

