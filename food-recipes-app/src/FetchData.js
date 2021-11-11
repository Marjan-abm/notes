/**
 * fetch data from web api using flask_app in api folder
 * @param {string} relUrl relative url of route
 * @param {string} meth CRUD method
 * @param {object} bd content of recipe details to put or post
 * @returns response
 */
async function FetchData(relUrl, meth, bd=null) {
  if (!bd) {
    // get, delete
    return fetch('http://127.0.0.1:5000/api/' + relUrl, {
      method: meth
    }).then((res) => res.json());
  }
  //put, post
  return fetch('http://127.0.0.1:5000/api/' + relUrl, {
    method: meth,
    headers: {
            'Content-Type': 'application/json'
        },
    body: JSON.stringify(bd)
  }).then((res) => res.json());
}

export default FetchData;