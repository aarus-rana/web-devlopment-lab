// var
var name = "Aarus Rana";
console.log("Var name:", name);

// let
let age = 19;
age = 20;
console.log("Let age:", age);

// const
const country = "Nepal";
console.log("Const country:", country);

//function
// takes a name argument and returns a greeting string prepended with "Hello "
function greet(name) {
    return "Hello " + name;
}

console.log(greet("lolol"));

//arrow function
// Ttakes two numbers, adds them, and returns their sum
const add = (a, b) => {
    return a + b;
};

console.log("Sum:", add(5, 3));

//object
const student = {
    name: "Aarus rana",
    age: 20,
    course: "web dev"
};

console.log(student.name);
console.log(student.course);

//map
const numbers = [1, 2, 3, 4];
//  callback function takes a number and returns its square
const squares = numbers.map(num => num * num);
console.log("Squares:", squares);

//filter
const nums = [10, 15, 20, 25];
//  callback function evaluates if the number is greater than 15
const result = nums.filter(num => num > 15);
console.log("Filtered:", result);

//spread operator
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5];
console.log(arr2)



//react js
//Arrow functions
// js
// component function conditionally returns a div based on the age variable, else it returns null
const myComp = () => {
    return age > 10 ? <div></div> : null;
}

//  anonymous function `()=>{console.log("hello")}` logs "hello" to the console when the button is clicked
// <button onClick={()=>{console.log("hello")}}> </button>annonymus function

// # ternary operators

let newAge = 10;
let newName = newAge > 10 && "pedro";
// ||
// ? if = : else =
// eg. let name2 =newAge>10 ? "aarus" : "rana"


// #objects 
const person = {
    name: "aarus",
    age: 20,
    isGoat: true
};
const pName = person.name //takes too much lines
// destruct Object a key var pair 

const { name: dName, age: dAge, isMaaried } = person;

const personObj = {
    name,
    age: 20,
    isGoat: true
};
const anotherName = "aaarus";

// inheritance 
const person2 = { ...personObj, name: "hello" }

const names = ["aarux", "raana"]
const names2 = [...names, "joe"] // addd elements to arrays inside states


let names3 = ["aarus", "arana"]
//  map function iterates over the names array, logs each name, and returns the name with "i" concatenated
names3.map((name) => {
    console.log(name);
    return name + "i"
})
//map function iterates over the names array and returns an h1 JSX element wrapping each name
names3.map((name) => {
    return <h1>{name}</h1>
})

let names4 = ["aarus", "aarus", "hehe"]
// filter function iterates over the names array and returns only the names that are not equal to "ped"
names4.filter((name) => {
    return name !== "hehe"
})

// async await fetch promise
// .reduce
// use let and consty because they are encloded within a block so more predictable behaviour less error prone
// but variable declared with var arew \\\