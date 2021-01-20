const form = document.querySelector('.rate-form')
const confirmBox = document.getElementById('confirm-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')


const handleStarSelect = (size) => {
	const stars = form.children //children - star
	for(let i=0; i <stars.length; i++){
		if(i <= size){
			stars[i].classList.add('checked')
		}	else {
			stars[i].classList.remove('checked')
		}
	}
}

const handleSelect = (selection) => {
	if(selection.substring(0,2) == 's-'){
		handleStarSelect(Number(selection[2]))
	}
}


const getNumericValue = (stringValue) =>{
	if(stringValue.substring(0,2) == 's-'){
		return Number(stringValue[2])
	}
	else {
		return 0
	}
}

if (document.getElementById('s-1')){

	const stars = [document.getElementById('s-1'),
					document.getElementById('s-2'),
					document.getElementById('s-3'),
					document.getElementById('s-4'),
					document.getElementById('s-5')]
					
	console.log(stars)
	stars.forEach(item=> item.addEventListener('mouseover', event=>{
		handleSelect(event.target.id)
	}))

	stars.forEach(item => item.addEventListener('click', (event)=>{

		let isSubmit = false //zmienna aby uniknąć kolizji
		form.addEventListener('submit', e=>{
			e.preventDefault()
			if(isSubmit){
				return
			}
			isSubmit = true

			$.ajax({
				type: 'POST',
				url: 'rate/',
				data: {
					'csrfmiddlewaretoken': csrf[0].value, // zdefiniowana wcześniej zmienna
					'rating_value': getNumericValue(event.target.id),
				},
				success: function(response){
					console.log(response)
					confirmBox.innerHTML =  `<p>You rated: ${response.score}</p>`
				},
				error: function(error){
					console.log(error)
					confirmBox.innerHTML = `<p>Oops... Something went wrong</p>`
				}
			})
		})
	}))
}