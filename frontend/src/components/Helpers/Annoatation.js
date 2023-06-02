export class Annotations {

    static getAnnotoriousAnnoations(rawAnnoations){
        const annos = []
        for(let i = 0; i<rawAnnoations.length; i++){
            if (rawAnnoations[i].type == 'char' || rawAnnoations[i].type == 'word' || rawAnnoations[i].type == 'tray' || rawAnnoations[i].type == 'mirrored' || rawAnnoations[i].type == 'barcode'|| rawAnnoations[i].type == 'label'){    
            let points = null

            const hasbox = 'box' in rawAnnoations[i];
            if(hasbox){
                points = rawAnnoations[i].box.reduce((acc, [x, y]) => {
                    return `${acc} ${x},${y}`;
                }, '');
            }

            const hasPL = 'polygon_list' in rawAnnoations[i];
            if(hasPL){
                points = rawAnnoations[i].polygon_list[0].reduce((acc, [x, y]) => {
                    return `${acc} ${x},${y}`;
                }, '');
            }
            
            if(!hasPL && !hasbox){
                continue
            }
            
            const svgPolygon = `<svg><polygon points="${points}" /></svg>`;

            annos.push({
                "id": "1",
                "type": "Annotation",
                "body": [{
                    "type": "TextualBody",
                    "purpose": "tagging",
                    "value": rawAnnoations[i].type,
                },{
                    "type": "TextualBody",
                    "purpose": "commenting",
                    "value": rawAnnoations[i].type
                }],
                "target": {
                    "selector": [{
                        "type": "SvgSelector",
                        "value": svgPolygon
                    }]
                }
            })

            }
        }
        return annos
    }
}