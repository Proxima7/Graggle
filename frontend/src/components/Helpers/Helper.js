
export class Helper {

    static base64_to_url(base64String ){
        // Convert base64 string to Blob
        const byteCharacters = atob(base64String.split(',')[1]);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: 'image/png' });

        // Create URL object from Blob
        const imageUrl = URL.createObjectURL(blob);
        return imageUrl
    }

}

export class Bookmark {

    static local_storace_name = 'bookmarks'

    static buildBookmark(store){
        return store.state.selected_db+'##'+store.state.selected_col
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
            bookmarksObjs.push({"database": bookmarkArray[0], "collection": bookmarkArray[1], "image": ""})
        }
        return bookmarksObjs
    }

    static setBookmarks(bookmarks){
        localStorage.setItem(Bookmark.local_storace_name, JSON.stringify(bookmarks));
    }

    static adjustCounter(store, amount_bookmarks){
        store.state.amount_bookmarks = amount_bookmarks       
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

