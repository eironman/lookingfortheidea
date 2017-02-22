var Helper = {

    // Function to get the security token to post with ajax
    getCookie: function(name)
    {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }

        return cookieValue;
    },

    // Returns a get parameter from the url
    getUrlParameter: function getUrlParameter(sParam)
    {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;

        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');

            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : sParameterName[1];
            }
        }
    },

    // Checks if a variable is empty
    isEmpty: function(data)
    {
        if (typeof data === 'number' || typeof data === 'boolean') {
          return false;
        }

        if (typeof(data) === 'undefined' || data === null) {
          return true;
        }

        if (typeof data.length !== 'undefined') {
          return data.length === 0;
        }

        var count = 0;
        for (var i in data) {
          if (data.hasOwnProperty(i)) {
            count++;
          }
        }

        return count === 0;
    },

    validateEmail: function(email) {
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
        }
    };