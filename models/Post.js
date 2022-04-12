const mongoose = require('mongoose');


require('mongoose-double')(mongoose);

var SchemaTypes = mongoose.Schema.Types;


// const OfferSchema = mongoose.Schema({
    

//     "investor":"string",

//     "amount": SchemaTypes.Double,

//     "equity": SchemaTypes.Double,

//     "comment":"string",
// })

const PitchSchema = mongoose.Schema({
   

    "entrepreneur":"string",

    "pitchTitle":"string",

    "pitchIdea":"string",

    "askAmount": SchemaTypes.Double,

    "equity": SchemaTypes.Double,

    "offers":[{
                "investor":"string",

            "amount": SchemaTypes.Double,

            "equity": SchemaTypes.Double,

            "comment":"string",
    }],
})

module.exports = mongoose.model('Pitches',PitchSchema)