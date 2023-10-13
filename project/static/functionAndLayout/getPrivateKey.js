        // Function to generate a random string of given length
        function generateRandomString(length) {
            const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
            let result = '';
            for (let i = 0; i < length; i++) {
                const randomIndex = Math.floor(Math.random() * characters.length);
                result += characters.charAt(randomIndex);
            }
            return result;
        }

        // Function to generate a formatted random string
        function generateFormattedRandomString() {
            const currentDate = new Date();
            const year = currentDate.getFullYear().toString().slice(-2);
            const month = ('0' + (currentDate.getMonth() + 1)).slice(-2);
            const day = ('0' + currentDate.getDate()).slice(-2);
            const hours = ('0' + currentDate.getHours()).slice(-2);
            const minutes = ('0' + currentDate.getMinutes()).slice(-2);
            const seconds = ('0' + currentDate.getSeconds()).slice(-2);
            const randomString = generateRandomString(8);

            return `${year}${month}${day}${hours}${minutes}${seconds}${randomString}@hamk.fi`;
        }

        // Function to generate and display the random string
        function generateAndDisplayRandomString() {
            const randomString = generateFormattedRandomString();
            const randomStringElement = document.getElementById('randomString');
            randomStringElement.innerText = `${randomString}`;
        }

        // Call the generateAndDisplayRandomString() function when the window has finished loading
        window.onload = generateAndDisplayRandomString;