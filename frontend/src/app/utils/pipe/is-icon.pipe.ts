import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'isIcon'
})
export class IsIconPipe implements PipeTransform {

  transform(value: string, args?: any): any {
    var isSupper = (value.toUpperCase() === value);
    var isAlpha = (value.search(/[^A-Za-z\s]/) == -1)
    return isAlpha && isSupper
  }

}
