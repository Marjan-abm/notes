import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import FetchData from '../FetchData';
import '../styles/Detail.css'

/**
 * Recipe detail in a table with button to add to or remove from favourite.
 * @returns Recipe detail react component
 */
const Detail = () => {
  // get id of recipe and table name
  let { id, table } = useParams();

  const [detail, setDetail] = useState(null);
  const [dataFav, setDataFav] = useState(null);
  
  // fetch data
  useEffect(() => {
  if (!detail) {
    async function getData() {
      const data = await FetchData(table + '?id=' + id, 'GET');
      if (!Object.prototype.hasOwnProperty.call(data, 'GET error')) {
        setDetail(data);
      }

      const dataFav = await FetchData('favourite?id=' + id, 'GET');
      if (!Object.prototype.hasOwnProperty.call(dataFav, 'GET error')) {
        setDataFav(dataFav);
      }
    }
    getData();
  }
  })

  /**
   * For the current recipe, add to or remove from favourite recipes table.
   * Reload page when clicked to show the updated text on the button.
   */
  const buttonHandler = async () => {
    if (dataFav) {
      // remove from fav table
      const data = await FetchData('favourite?id=' + id, 'DELETE');
      console.log(data);
    } else {
      // add to fav table
      const data = await FetchData('favourite?id=' + id, 'POST', detail);
      console.log(data);
    }
    window.location.reload();
  }

  // data is not loaded
  if (!detail) {
    return (
      <div>
        Recipe not found
      </div>
    )
  }
  
  // html content of detail of recipe
  return (
    <div>
      <div className='table-container'>
        <table className='table-detail'>
          <tbody>
            <tr className='tr-detail'>
              <td className='td-detail' colSpan='2'><img src={detail['image url']} alt='' /></td>
            </tr>
            <tr className='tr-detail'>
              <td className='td-detail'>{'Name: ' + (detail.name ? detail.name : 'unknown')}</td>
              <td className='td-detail'>{'ID: ' + (detail.id ? detail.id : 'unknown')}</td>
            </tr>
            <tr className='tr-detail'>
              <td className='td-detail' colSpan='2'>{detail.description ? detail.description: 'unknown'}</td>
            </tr>
            <tr className='tr-detail'>
              <td className='td-detail'>{'Yields: ' + (detail.yields ? detail.yields : '1')}</td>
              <td className='td-detail'>{'Popularity: ' + (detail.popularity ? detail.popularity : '0')}</td>
            </tr>
            <tr className='tr-detail'>
              <td className='td-detail'>{'Prep Time: ' + (detail['prep time'] ? detail['prep time'] + ' mins': 'unknown')}</td>
              <td className='td-detail'>{'Cook Time: ' + (detail['cook time'] ? detail['cook time'] + ' mins': 'unknown')}</td>
            </tr>
            <tr className='tr-detail'>
              <td className='td-detail' colSpan='2'>
              <ul className='ul-meal-types'>
                Meal Types: 
                {detail['meal types'].map((mealType, index) => {
                  return (<li key={index}>{mealType}</li>)
                })}
              </ul>
              </td>
            </tr>
            <tr className='tr-detail'>
              <td className='td-detail'>Ingredients: </td>
              <td className='td-detail'>Instructions: </td>
            </tr>
            <tr className='tr-detail'>
              <td className='td-detail'>
              <ul className='ul-ingredients'>
                {detail.ingredients.map((ingredient, index) => {
                  return (<li key={index}>{ingredient}</li>)
                })}
              </ul>
              </td>

              <td className='td-detail'>
              <ol className='ol-instructions'>
                {detail.instructions.map((instruction, index) => {
                  return (<li key={index}>{instruction}</li>)
                })}
              </ol>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div className='button-container'>
        <button className='button-add-remove-fav' onClick={buttonHandler}>{dataFav ? 'Remove From Favourite' : 'Add To Favourite'}</button>
      </div>
    </div>
  )
}

export default Detail;