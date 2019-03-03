import React from 'react';
import { getAllImages } from '../../api/apiClient';
import { Image } from '../../types';

interface State {
  images: Array<Image>;
}

export class Admin extends React.Component<State> {
  state: State = {
    images: []
  };

  componentDidMount() {
    getAllImages()
      .catch(e => {
        console.log('error', e);
      })
      .then((response: Response) => {
        console.log('==== response', response);
        return response.json();
      })
      .then(json => {
        console.log(JSON.stringify(json));
      });
  }

  renderImageList = (images: Array<Image>) => {
    return (
      <ul>
        {images.map(image => (
          <li>{image.url}</li>
        ))}
      </ul>
    );
  };

  render() {
    const { images } = this.state;
    if (images.length === 0) return <div>No images</div>;
    return this.renderImageList(images);
  }
}
