import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'typeName'
})
export class TypeNamePipe implements PipeTransform {

  transform(value: string, args?: any): string {
    let name = '';
    switch (value) {
      case 'A':
        name = 'ATV';
        break;
      case 'V':
        name = 'Automobile';
        break;
      case 'M':
        name = 'Boat';
        break;
      case 'D':
        name = 'Dirt Bike';
        break;
      case 'U':
        name = 'Heavy Duty Trucks';
        break;
      case 'E':
        name = 'Industrial Equipment';
        break;
      case 'J':
        name = 'Jet Ski';
        break;
      case 'K':
        name = 'Medium Duty/Box Trucks';
        break;
      case 'C':
        name = 'Motorcycle';
        break;
      case 'R':
        name = 'Recreational Vehicle (RV)';
        break;
      case 'S':
        name = 'Snowmobile';
        break;
      case 'L':
        name = 'Trailers';
        break;
      default:
        name = value;
    }
    return name;
  }

}
