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