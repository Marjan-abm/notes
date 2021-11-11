import { useRef, useState } from 'react';
import FetchData from '../FetchData';
import '../styles/UpdateForm.css';

/**
 * Update forms that includes inputs for all the fields of recipes, supporting put, post, or delete by id.
 * @returns Update form react component
 */
const UpdateForm = () => {
  const [response, setResponse] = useState([]);

  const id = useRef();
  const name = useRef();
  const imageUrl = useRef();
  const description = useRef();
  const yields = useRef();
  const prepTime = useRef();
  const cookTime = useRef();
  const mealTypes = useRef();
  const ingredients = useRef();
  const instructions = useRef();

  /**
   * Update the all recipes table from user input using form.
   * @param {string} method CRUD method to perform
   */
  const update = async (method) => {
    // get values in the form
    const idInput = id.current.value;
    const nameInput = name.current.value;
    const imageUrlInput = imageUrl.current.value;
    const descriptionInput = description.current.value;
    const yieldsInput = yields.current.value;
    const prepTimeInput = prepTime.current.value;
    const cookTimeInput = cookTime.current.value;
    const mealTypesInput = mealTypes.current.value;
    const ingredientsInput = ingredients.current.value;
    const instructionsInput = instructions.current.value;

    const mealTypesList = mealTypesInput ? mealTypesInput.split('\n') : ['unknown'];
    const ingredientsList = ingredientsInput ? ingredientsInput.split('\n') : ['unknown'];
    const instructionsList = instructionsInput ? instructionsInput.split('\n') : ['unknown'];

    // add key value pairs to recipe object
    let recipeObj = {}
    if (nameInput) recipeObj.name = nameInput;
    if (imageUrlInput) recipeObj['image url'] = imageUrlInput;
    if (descriptionInput) recipeObj.description = descriptionInput;
    if (yieldsInput) recipeObj.yields = yieldsInput;
    if (prepTimeInput) recipeObj['prep time'] = prepTimeInput;
    if (cookTimeInput) recipeObj['cook time'] = cookTimeInput;
    recipeObj['meal types'] = mealTypesList;
    recipeObj.ingredients = ingredientsList;
    recipeObj.instructions = instructionsList;

    // fetch according to different method
    let res = null;
    switch (method) {
      case 'PUT':
        res = await FetchData('food?id=' + idInput, method, recipeObj);
        break;
      case 'POST':
        recipeObj.id = idInput;
        res = await FetchData('food', method, recipeObj);
        break
      case 'DELETE':
        res = await FetchData('food?id=' + idInput, method);
        break;
      default:
        console.log('Internal error: method not valid');
    }

    // set response that will be used to display
    setResponse([]);
    for (const [key, value] of Object.entries(res)) {
      setResponse(preRes => [...preRes, key + ': ' + value]);
    }
  }

  return (
    <div className='update-form-container'>
      {/* form used to update all recipes table in database */}
      <form className='form-update'>
        <table className='table-update'>
          <tbody>
            <tr className='tr-update-form'>
              <td className='td-update-form'><label className='id'>ID: </label></td>
              <td className='td-update-form'><input className='input-update' type='text' id='id' name='id' ref={id}/></td>
            </tr>
            <tr className='tr-update-form'>
              <td className='td-update-form'><label className='name'>Name: </label></td>
              <td className='td-update-form'><input className='input-update' type='text' id='name' name='name' ref={name}/></td>
            </tr>
            <tr className='tr-update-form'>
              <td className='td-update-form'><label className='image-url'>Image url: </label></td>
              <td className='td-update-form'><input className='input-update' type='text' id='image-url' name='image url' ref={imageUrl}/></td>
            </tr>
            <tr className='tr-update-form'>
              <td className='td-update-form'><label className='yields'>Yields: </label></td>
              <td className='td-update-form'><input className='input-update' type='text' id='yields' name='yields' ref={yields}/></td>
            </tr>
            <tr className='tr-update-form'>
              <td className='td-update-form'><label className='prep-time'>Prep Time: </label></td>
              <td className='td-update-form'><input className='input-update' type='text' id='prep-time' name='prep time' ref={prepTime}/></td>
            </tr>
            <tr className='tr-update-form'>
              <td className='td-update-form'><label className='cook-time'>Cook Time: </label></td>
              <td className='td-update-form'><input className='input-update' type='text' id='cook-time' name='cook time' ref={cookTime}/></td>
            </tr>
            <tr className='tr-update-form'>
              <td className='td-update-form'><label className='description'>Description: </label></td>
              <td className='td-update-form'><input className='input-update' type='text' id='description' name='description' ref={description}/></td>
            </tr>
            <tr className='tr-update-form'>
              <td className='td-update-form'><label className='meal-types'>Meal Types: </label></td>
              <td className='td-update-form'><textarea className='textarea' type='text' id='meal-types' name='meal types' ref={mealTypes}/></td>
            </tr>
            <tr className='tr-update-form'>
              <td className='td-update-form'><label className='ingredients'>Ingredients: </label></td>
              <td className='td-update-form'><textarea className='textarea' type='text' id='ingredients' name='ingredients' ref={ingredients}/></td>
            </tr>
            <tr className='tr-update-form'>
              <td className='td-update-form'><label className='instructions'>Instructions: </label></td>
              <td className='td-update-form'><textarea className='textarea' type='text' id='instructions' name='instructions' ref={instructions}/></td>
            </tr>
          </tbody>
        </table>

        <div>
          <button className='button-update' onClick={(e) => {
            e.preventDefault();
            update('PUT');
          }}>Update</button>

          <button className='button-update' onClick={(e) => {
            e.preventDefault();
            update('POST');
          }}>Append</button>

          <button className='button-update' onClick={(e) => {
            e.preventDefault();
            update('DELETE');
          }}>Delete By ID</button>
        </div>
      </form>
      
      {/* success and error message */}
      <div className='message'>
        {response.map(res => {
          return (<div>{res}<br/></div>)
        })}
      </div>
    </div>
  )
}

export default UpdateForm;