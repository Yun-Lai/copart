import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'getHighlight'
})
export class GetHighlightPipe implements PipeTransform {

  transform(value: string, args?: string): any {
    let name = '';
    switch (value) {
      case 'R':
        name = 'Run & Drive';
        break;
      case 'C':
        name = 'Seller Certified';
        break;
      case 'E':
        name = 'Enhanced Vehicle';
        break;
      // case 'C':
      //   name = 'CrashedToys'
      //   break;
      case 'S':
        name = 'Engine Start Program';
        break;
      case 'F':
        name = 'Featured Vehicle';
        break;
      case 'O':
        name = 'Offsite Sales';
        break;
      case 'D':
        name = 'Donated Vehicle';
        break;
      case 'Q':
        name = 'Donated Vehicle';
        break;
      case 'B':
        name = 'Sealed Bid Repossession';
        break;
      case 'V':
        name = 'VIX';
        break;
      // case 'F':
      //   name = 'FAST';
      //   break;
      case 'H':
        name = 'Hybrid Vehicles';
        break;
      default:
        name = value;
    }
    return name;
  }

}
