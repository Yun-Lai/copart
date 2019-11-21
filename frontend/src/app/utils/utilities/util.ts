export class Util {

  public static isNullOrUndefined(value: any): boolean {
    return value === null || value === undefined;
  }

  public static hasContent(value: any): boolean {
    return !Util.isNullOrUndefined(value) && value.length > 0;
  }

  public static isNumber(value: any): boolean {
    return typeof value === 'number';
  }

  public static tryJsonParse(data: string): any {
    try {
      return JSON.parse(data);
    } catch (error) {
      console.error('JSON.parse() failed. ' + error);
      return null;
    }
  }

  public static extractErrorMessage(error: any): string {
    if (Util.isNullOrUndefined(error)) {
      return 'Error Occurred';
    }
    if (!Util.isNullOrUndefined(error['message'])) {
      return error.message;
    }
    if (!Util.isNullOrUndefined(error['text'])) {
      return error.text;
    }
    return typeof error === 'string' ? error : 'Error Occurred'
  }

  public static areNumbersEqual(v1: number | string, v2: number | string): boolean {
    if (!Util.isNumber(v1)) {
      v1 = parseInt(v1.toString(), 0);
    }

    if (!Util.isNumber(v2)) {
      v2 = parseInt(v2.toString(), 0)
    }
    return v1 === v2;
  }
}
