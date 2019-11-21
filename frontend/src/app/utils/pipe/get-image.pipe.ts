import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'getImage'
})
export class GetImagePipe implements PipeTransform {

  transform(value: string, index: number): any {
    return 'https://cs.copart.com/v1/AUTH_svc.pdoc00001/' + value.split('|')[index];
  }
}
