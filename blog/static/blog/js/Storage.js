// Stores data in local storage
var Storage = {

  get: function(key, parseJson)
  {
    console.log('[GET] ' + key);
    parseJson = parseJson || false;

    var value = window.localStorage.getItem(key);
    if (parseJson && value !== null) {
      value = JSON.parse(value);
    }

    return value;
  },

  remove: function(key)
  {
    console.log('[DELETE] ' + key);
    window.localStorage.removeItem(key);
  },

  set: function(key, value) {
    console.log('[SET] ' + key + ' - ' + value.substring(0, 100));
    window.localStorage.setItem(key, value);
  }
}