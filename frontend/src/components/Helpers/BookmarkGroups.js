export class BookmarkGroups {

    static local_storace_name = 'bookmarkgroups'


    static _getBookmarkGroups( ){
        const groups = JSON.parse(localStorage.getItem(BookmarkGroups.local_storace_name)) || [];
        return groups
    }

    static _setBookmarkGroups( ){
        const groups = [
            {"title": "fruit", "datasets": [{"db": "fruit-recognition", "col": "fruits360" }, {"db": "fruit-recognition", "col": "fruits_on_plate" }]},
            {"title": "hornbach", "datasets": [{"db": "object-recognition", "col": "Hornbach-data-bornheim" }]}
        ]
        localStorage.setItem(BookmarkGroups.local_storace_name, JSON.stringify(groups));
    }

    static _createBookmarkGroup(name, db, col){
        let groups = this._getBookmarkGroups()
        groups.push({"name": name, "datasets": [{"db": db, "col": col }]})
        localStorage.setItem(BookmarkGroups.local_storace_name, JSON.stringify(groups));
    }

    static adjustCounter(store){
        store.amount_bookmark_groups = store.amount_bookmark_groups+1       
    }


    static _add2BookmarkGroup(name, db, col){
        let groups = this._getBookmarkGroups()
        for(let i=0; i<groups.length; i++){
            if(groups[i].name == name){
                groups[i].datasets.push({"db": db, "col": col })
            }
        }
        localStorage.setItem(BookmarkGroups.local_storace_name, JSON.stringify(groups));
    }

    static _removeBookmarkGroup(name, db, col){
        let groups = this._getBookmarkGroups()
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
        localStorage.setItem(BookmarkGroups.local_storace_name, JSON.stringify(groups));
    }
    
    static addBookmarkGroup(name, db, col, store){
        this.adjustCounter(store)
        return this. _add2BookmarkGroup(name, db, col)
    }

    static removeBookmarkGroup(name, db, col, store){
        this.adjustCounter(store)
        return this. _removeBookmarkGroup(name, db, col)
    }
    

    static setBookmarkGroup(name, db, col, store){
        this.adjustCounter(store)
        return this. _createBookmarkGroup(name, db, col)
    }

    static getBookmarkGroups(db, col){
        let bookmarkgroups = this._getBookmarkGroups()
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

