import * as d3 from 'd3';
import { useRef, useState, useEffect } from 'react';
import '../styles/Chart.css';
import FetchData from '../FetchData';

/**
 * Bar chart displayed in tab 4
 * @returns chart react component
 */
const Chart = () => {
  const inputK = useRef();
  const fieldSelected = useRef();
  const orderSelected = useRef();

  const [hasLoadedAll, setHasLoadedAll] = useState(false);
  const [allRecipes, setAllRecipes] = useState([]);

  // fetch data of all recipes
  useEffect(() => {
    if (!hasLoadedAll) {
    async function getData() {
      const dataAll = await FetchData('search?q=all.name:', 'GET');
      if (!Object.prototype.hasOwnProperty.call(dataAll, 'GET error')) {
        setAllRecipes(dataAll);
      }
    }
    getData();
    setHasLoadedAll(true);
  }
  }, [hasLoadedAll, setHasLoadedAll, setAllRecipes]);

  /**
   * Function for draw button.
   * Get the dict of recipes needed to show.
   * Then sort the recipes by field value.
   * Then visualize the data using bar chart.
   */
  const draw = async () => {
    // get input values
    const k = inputK.current.value;
    const field = fieldSelected.current.value;
    const order = orderSelected.current.value;

    let dataset = [];
    // determine the number of recipes to show
    let targetK = k;
    if (allRecipes.length < k) {
      targetK = allRecipes.length;
    }
    console.log(allRecipes.length);
    // retrive only name and field key value pairs from original dict
    for (let i = 0; i < allRecipes.length; i += 1) {
      const doc = allRecipes[i];
      if (field in doc) {
        const newDoc = {};
        newDoc.name = doc['name'];
        newDoc[field] = doc[field];
        dataset.push(newDoc);
      }
    }
    // get sorted data by value in field
    let sortedDataset = quicksort(dataset, field);
    if (order === 'desc') {
      // reverse the order
      sortedDataset = sortedDataset.reverse();
    }
    if (sortedDataset.length > targetK) {
      // get the targetK number of recipes starting from the front
      sortedDataset = sortedDataset.slice(0, targetK);
    }
    visualize(sortedDataset, field);
  }

  /**
   * sort the array in ascending order
   * @param {list} array 
   * @param {string} field 
   * @returns sorted array
   */
  const quicksort = (array, field) => {
    if (array.length <= 1) {
      return array;
    }
    const left = [];
    const right = [];
    const pivot = array[0];
    const pivotVal = Number(pivot[field]);
    for (let i = 1; i < array.length; i++) {
      Number(array[i][field]) < pivotVal ? left.push(array[i]) : right.push(array[i]);
    }
    return quicksort(left, field).concat(pivot, quicksort(right, field));
  }

  /**
   * visualize the dataset using bar chart with svg
   * @param {list} dataset list of dict
   * @param {string} field key in the dict to order
   */
  const visualize = (dataset, field) => {
    console.log(dataset);
    // find the max value of all field values
    const maxFieldValue = Math.max.apply(Math, dataset.map(function(o) { return o[field]; }));
    // List to store labels in x-axis, which are recipe names
    let xLabels = [];
    // Set used to store names to check repeated names
    let nameSet = new Set();
    for (let i = 0; i < dataset.length; i++) {
      if (nameSet.has(dataset[i]['name'])) {
        // name is repeated, set new name
        const newName = dataset[i]['name'] + '*';
        nameSet.add(newName);
        xLabels.push(newName);
      } else {
        nameSet.add(dataset[i]['name']);
        xLabels.push(dataset[i]['name']);
      }
    }
    //remove previous chart and create a new one
    d3.select('svg').remove();
    d3.select('.svg-container').append('svg');

    // chart width
    const svgWidth = 1000;
    // chart height
    const svgHeight = 500;
    // x coordinate of chart relative to the original position
    const yAxisPosX = 30;
    // distance of bars up to the x-axis
    const xAxisBarGap = svgHeight * 0.1;
    // width of each bar
    const barWidth = (svgWidth - yAxisPosX) / dataset.length;
    // distance between bars
    const barPadding = barWidth * 0.2;

    const svg = d3.select('svg')
      .attr('width', svgWidth)
      .attr('height', svgHeight);

    const yScale = d3.scaleLinear()
      .domain([0, maxFieldValue])
      .range([0, svgHeight * 0.8]);

    // bar chart
    svg.selectAll('rect')
      .data(dataset)
      .enter()
      .append('rect')
      .attr('y', function(d) {
          return svgHeight - xAxisBarGap - yScale(Number(d[field]));
      })
      .attr('height', function(d) {
          return yScale(Number(d[field]));
      })
      .attr('width', barWidth - barPadding)
      .attr('transform', function(d, i) {
          const translate = [barWidth * i + yAxisPosX + 5, 0]
          return 'translate(' + translate + ')'
      });

    // text
    svg.selectAll('text')
      .data(dataset)
      .enter()
      .append('text')
      .text(function(d) {
          return d[field]
      })
      .attr('y', function(d, i) {
          return svgHeight * 0.9 - yScale(Number(d[field])) - 2;
      })
      .attr('x', function(d, i) {
          return barWidth * i + barWidth * 0.2 + yAxisPosX;
      })
      .attr('fill', '#A64C38');

    // Axes
    const yAxisScale = d3.scaleLinear()
      .domain([0, maxFieldValue])
      .range([svgHeight * 0.8, 0]);

    const yAxis = d3.axisLeft()
      .scale(yAxisScale);

    svg.append('g')
      .attr('transform', 'translate(' + yAxisPosX + ',' + svgHeight * 0.1 + ')')
      .call(yAxis);

    const xAxisScale = d3.scalePoint()
      .domain(xLabels)
      .range([barWidth * 0.5, svgWidth - barWidth * 0.5 - yAxisPosX]);

    const xAxis = d3.axisBottom()
        .scale(xAxisScale)
        .ticks(xLabels.length);

    const xAxisGroup = svg.append('g')
      .attr('transform', 'translate(' + yAxisPosX + ',' + svgHeight * 0.9 + ')')
      .call(xAxis);
    // rotate labels in x-axis
    xAxisGroup.selectAll('text')
      .attr('transform', 'translate(0, 10) rotate(-20)');
  }

  return (
    <div>
      <div>
        <form>
          <label>Field:</label>
          <select className='select-bar-chart' name='select-field' id='select-field' ref={fieldSelected}>
            <option value='yields'>Yields</option>
            <option value='prep time'>Prep Time</option>
            <option value='cook time'>Cook Time</option>
            <option value='popularity'>Popularity</option>
          </select>

          <label>Order:</label>
          <select className='select-bar-chart' name='select-order' id='select-order' ref={orderSelected}>
            <option value='ascd'>Ascending</option>
            <option value='desc'>Descending</option>
          </select>

          <br/>

          <label>Number of top recipes: </label>
          <input id='input-k' type='text' ref={inputK}/>

          <button className='button-draw' id='button-draw' onClick={(e) => {
            e.preventDefault();
            draw();
            }}>Draw</button>
        </form>
      </div>

      <div className='svg-container'>
        <svg className='bar-chart'></svg>
      </div>

      <script src='https://d3js.org/d3.v7.min.js'></script>
    </div>
  )

}

export default Chart;
