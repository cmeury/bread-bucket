const URL = window.location;
const BASE_URL = URL.protocol + '//' + URL.host;

async function getData(url = '') {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'GET',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json'
    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer'
  });
  return response.json();
}

export default async function getMemosBySubtext(memoSubText='') {
    const apiEndpoint = `${BASE_URL}/transactions/memos/${memoSubText}`;
    try {
        return getData(apiEndpoint);
    } catch(err) {
        console.log(err);
        throw(err);
    }
}
