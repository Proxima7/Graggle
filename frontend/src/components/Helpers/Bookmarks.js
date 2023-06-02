export class Bookmark {

    static local_storace_name = 'bookmarks'

    static buildBookmark(store){
        return store.selected_db+'##'+store.selected_col
    }

    static getBookmarks( ){
        const bookmarks = JSON.parse(localStorage.getItem(Bookmark.local_storace_name)) || [];
        return bookmarks
    }

    static getBookmarksObj( ){
        const bookmarks = JSON.parse(localStorage.getItem(Bookmark.local_storace_name)) || [];
        const bookmarksObjs = [];

        for(let i = 0; i<bookmarks.length; i++){
            const bookmarkArray = bookmarks[i].split("##")
            bookmarksObjs.push({"database": bookmarkArray[0], "collection": bookmarkArray[1], "image": "", "title": ""})
        }
        return bookmarksObjs
    }

    static setBookmarks(bookmarks){
        localStorage.setItem(Bookmark.local_storace_name, JSON.stringify(bookmarks));
    }

    static adjustCounter(store, amount_bookmarks){
        store.amount_bookmarks = amount_bookmarks       
    } 

    static bookmark(store){
        const bookmark = this.buildBookmark(store)
        const bookmarks = this.getBookmarks()
        bookmarks.push(bookmark);
        this.setBookmarks(bookmarks)        
        this.adjustCounter(store,bookmarks.length)
    }

    static unbookmark(store){
        const bookmark = this.buildBookmark(store)
        const bookmarks = this.getBookmarks()
        const bookmarksindex = bookmarks.indexOf(bookmark);
        if (bookmarksindex > -1) {
            bookmarks.splice(bookmarksindex, 1);
        }
        this.setBookmarks(bookmarks) 
        this.adjustCounter(store,bookmarks.length)
    }

    static isbookmarked(store){
        const bookmark = this.buildBookmark(store)
        const bookmarks = this.getBookmarks()
        const bookmarksindex = bookmarks.indexOf(bookmark);
        if (bookmarksindex > -1) {
            return true
        }
        return false
    }

}

