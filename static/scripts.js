// register modal component
 Vue.component("modal", {
   template: "#modal-template"
 });

var app = new Vue({
  el: "#app",

  //------- data --------
  data: {
    serviceURL: "https://cs3103.cs.unb.ca:8010",
    authenticated: false,
    urls: [],
    loggedIn: null,
    input: {
      username: "",
      password: ""
    },
    language: {
      english:"En",
      french:"Fr"
    }

  },
  //------- lifecyle hooks --------
  mounted: function() {
    axios
    .get(this.serviceURL+"/validate_session")
    .then((response) => {
      if(response.data.isAuthenticated){
        this.authenticated = true;
        this.loggedIn = response.data.userID;
        this.fetchUrls();
      }
    })
    .catch((error) => {
        this.authenticated = false;
        console.log(error);
    });
  },
  //------- methods --------
  methods: {
    login() {
      if (this.input.username != "" && this.input.password != "") {
        axios
        .post(this.serviceURL+"/signin", {
            "username": this.input.username,
            "password": this.input.password
        })
        .then((response) => {
            if (response.data.Authentication === "success") {
              this.authenticated = true;
              this.loggedIn = response.data.userID;
            //  localStorage.setItem('sessionToken', response.data.sessionToken);
              localStorage.setItem('username', response.data.user)
              this.fetchUrls();
            }
            else{
              this.authenticated = false
            }
        })
        .catch((e) => {
            alert("The username or password was incorrect, try again");
            this.input.password = "";
            console.log(e);
        });
      } else {
        alert("A username and password must be present");
      }
    },

    addURL() {
      try {
        new URL(this.input.originalURL);
        // If the URL is valid, call the api endpoint to add the url.      
        axios
        .post(this.serviceURL + "/users/" + this.loggedIn + "/link",
        {
          "originalURL": this.input.originalURL
        })
        .then((response) => {
          this.input.originalURL = '';
          this.fetchUrls();
        })
        .catch((error) => {
            console.log(error);
        });

    } catch (error) {
        if (error instanceof TypeError) {
            alert("Please enter a valid URL.");
        } else {
            console.error("An unexpected error occurred: ", error);
        }
    }
    

    },

    deleteURL(url_id) {
      // Ask for confirmation before deleting
      if (confirm("Are you sure you want to delete this URL?")) {
          axios
          .delete(this.serviceURL + "/users/" + this.loggedIn + "/links/" +url_id)
          .then((response) => {
              this.fetchUrls();
          })
          .catch((error) => {
              console.log(error);
          });
      }
  },

    deleteUser() {
      axios
      .delete(this.serviceURL + "/delete_user/" + this.loggedIn)
      .then((response) => {
        localStorage.setItem('username' , '');
        location.reload();
      })
      .catch((error) => {
        console.warn(error)
      })
    },

    editURL(shortURL, linkID) {
      const newAlias = prompt("ENTER NEW ALIAS")
      if(newAlias) {
        const lastPartOfURL = shortURL?.split('/')?.slice(-1)[0]
        // Regex to check for a slash anywhere in the string
        const slashRegex = /\//;
        if (slashRegex.test(newAlias)) {
            alert("Alias cannot contain a slash ('/') character. Please enter a simple string for eg 'test'.");
            return; // Exit the function if slash is found
        }
        axios
        .put(this.serviceURL + "/users/" + this.loggedIn + "/links/" +linkID, {"alias" : newAlias})
        .then((response) => {
          this.fetchUrls();
        })
        .catch((error) => {
          alert("Please try a different alias. That alias was either already taken by another user or invlaid.");
          console.log(error);
        });
      }

    },

    fetchUrls() {
      axios
      .get(this.serviceURL + "/users/" + this.loggedIn + "/links")
      .then((response) => {
            this.urls = response.data;
            this.input.username = localStorage.getItem('username');
      })
      .catch((error) => {
          console.log(error);
      });
    },

    copyToClipboard(text) {
      navigator.clipboard.writeText("https://cs3103.cs.unb.ca:8010/" + text).then(() => {
          alert('Text copied to clipboard!');
      }).catch(err => {
          console.error('Could not copy text: ', err);
      });
    },

    logout() {
      axios
      .delete(this.serviceURL+"/signin")
      .then((response) => {
        location.reload();
      })
      .catch((e) => {
        console.log(e);
      });
    },
  }
  //------- END methods --------

});
