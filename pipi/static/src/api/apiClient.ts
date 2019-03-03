// TODO: setup proper uri
const BASE_URI = 'http://localhost:5000';

export function getAllImages(): Promise<Response> {
  return fetch(`${BASE_URI}/images`);
}
